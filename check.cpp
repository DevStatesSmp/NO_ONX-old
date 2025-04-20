#include <iostream>
#include <fstream>
#include <sys/inotify.h>
#include <unistd.h>
#include <fcntl.h>
#include <cstring>
#include <dirent.h>
#include <sys/stat.h>
#include <string>
#include <map>
#include <signal.h>
#include <ctime>
#include <cerrno>

#define MAX_EVENTS 1024
#define LEN_NAME 256
#define EVENT_SIZE (sizeof(struct inotify_event))
#define BUF_LEN (MAX_EVENTS * (EVENT_SIZE + LEN_NAME))

std::map<int, std::string> watch_map;
bool running = true;
std::ofstream log_file("watcher.log");

// ANSI color codes
#define RED     "\033[91m"
#define GREEN   "\033[92m"
#define YELLOW  "\033[93m"
#define CYAN    "\033[96m"
#define RESET   "\033[0m"

// Timestamp
std::string current_time() {
    time_t now = time(nullptr);
    char buf[32];
    strftime(buf, sizeof(buf), "%Y-%m-%d %H:%M:%S", localtime(&now));
    return std::string(buf);
}

// Logging
void log_event(const std::string& level, const std::string& event_type, const std::string& path) {
    std::string color;
    if (level == "INFO") color = GREEN;
    else if (level == "WARN") color = YELLOW;
    else if (level == "ALERT") color = RED;
    else color = CYAN;

    std::string time_str = current_time();
    std::string msg = "[" + level + "] [" + time_str + "] " + event_type + " -> " + path;

    std::cout << color << msg << RESET << std::endl;
    log_file << msg << std::endl;
}

// Show permission fix instructions
void print_permission_tutorial(const std::string& denied_path) {
    std::cerr << YELLOW << "\n[!] Permission denied while accessing: " << denied_path << RESET << std::endl;

    std::cerr << CYAN << "\n[💡 HOW TO FIX PERMISSION ISSUE]\n" << RESET;
    std::cerr << "🔐 You may need elevated privileges to access this directory.\n";
    std::cerr << GREEN << "👉 Try running this program with sudo:\n";
    std::cerr << "   sudo ./no_onx_watcher " << denied_path << RESET << "\n";

    std::cerr << CYAN << "\n[📦 INSTALL INOTIFY IF MISSING]\n" << RESET;
    std::cerr << "For Debian/Ubuntu:\n" << GREEN << "   sudo apt install libinotifytools0-dev\n" << RESET;
    std::cerr << "For Arch Linux:\n" << GREEN << "   sudo pacman -S inotify-tools\n" << RESET;
    std::cerr << std::endl;
}

// Recursive watcher
void watch_directory(int fd, const std::string& path) {
    DIR *dir = opendir(path.c_str());
    if (!dir) {
        if (errno == EACCES) {
            print_permission_tutorial(path);
        } else {
            log_event("WARN", "Failed to open directory", path);
        }
        return;
    }

    struct dirent *entry;
    while ((entry = readdir(dir)) != nullptr) {
        if (entry->d_name[0] == '.') continue;

        std::string file_path = path + "/" + entry->d_name;
        struct stat file_stat;
        if (stat(file_path.c_str(), &file_stat) == 0) {
            if (S_ISDIR(file_stat.st_mode)) {
                int wd = inotify_add_watch(fd, file_path.c_str(), IN_CREATE | IN_MODIFY | IN_DELETE | IN_MOVED_FROM | IN_MOVED_TO);
                if (wd != -1) {
                    watch_map[wd] = file_path;
                    log_event("INFO", "Watching directory", file_path);
                    watch_directory(fd, file_path); // recurse
                } else {
                    if (errno == EACCES) {
                        print_permission_tutorial(file_path);
                    } else {
                        log_event("WARN", "Failed to add watch", file_path);
                    }
                }
            }
        }
    }
    closedir(dir);
}

// Handle Ctrl+C
void signal_handler(int sig) {
    std::cout << "\n" << RED << "[!] Termination signal received. Shutting down..." << RESET << std::endl;
    running = false;
}

// Event handler
void handle_events(int fd) {
    char buffer[BUF_LEN];
    ssize_t length;

    while (running) {
        length = read(fd, buffer, BUF_LEN);
        if (length < 0) {
            perror("read");
            break;
        }

        int i = 0;
        while (i < length) {
            struct inotify_event *event = (struct inotify_event *)&buffer[i];
            std::string watched_path = watch_map[event->wd];
            std::string file_path = watched_path + "/" + event->name;

            if (event->mask & IN_CREATE) {
                log_event("INFO", "Created", file_path);

                // Auto-watch new dirs
                struct stat st;
                if (stat(file_path.c_str(), &st) == 0 && S_ISDIR(st.st_mode)) {
                    int wd = inotify_add_watch(fd, file_path.c_str(), IN_CREATE | IN_MODIFY | IN_DELETE | IN_MOVED_FROM | IN_MOVED_TO);
                    if (wd != -1) {
                        watch_map[wd] = file_path;
                        log_event("INFO", "Now watching", file_path);
                        watch_directory(fd, file_path);
                    }
                }
            }
            if (event->mask & IN_DELETE)
                log_event("WARN", "Deleted", file_path);
            if (event->mask & IN_MODIFY)
                log_event("INFO", "Modified", file_path);
            if (event->mask & IN_MOVED_FROM)
                log_event("ALERT", "Moved From", file_path);
            if (event->mask & IN_MOVED_TO)
                log_event("INFO", "Moved To", file_path);

            i += EVENT_SIZE + event->len;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << RED << "Usage: " << argv[0] << " <directory_to_watch>" << RESET << std::endl;
        return 1;
    }

    if (geteuid() != 0) {
        std::cerr << YELLOW << "[!] You are not running as root. Some directories may be inaccessible.\n" << RESET;
    }

    signal(SIGINT, signal_handler);

    std::string target_dir = argv[1];
    int fd = inotify_init1(IN_NONBLOCK);
    if (fd < 0) {
        std::cerr << RED << "Failed to initialize inotify" << RESET << std::endl;
        return 1;
    }

    std::cout << CYAN << "===[ NO_ONX FILE MONITOR STARTED ]===\n" << RESET;
    log_event("INFO", "Monitoring started at", target_dir);

    watch_directory(fd, target_dir);
    handle_events(fd);

    close(fd);
    log_event("INFO", "Monitoring stopped", target_dir);
    log_file.close();

    return 0;
}


