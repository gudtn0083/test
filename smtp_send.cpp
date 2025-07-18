// smtp_send.cpp
// Compile with: g++ -std=c++17 smtp_send.cpp -lcurl -o smtp_send
//
// Simple example of sending an email using libcurl's SMTP capabilities.
// This code sends a plain-text email via STARTTLS (port 587).
//
// Note: You may need to allow "Less secure app access" or use an App Password
// with Gmail accounts.

#include <curl/curl.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <iostream>
#include <string>
#include <vector>

// Helper structure to feed the email payload to libcurl
struct UploadContext {
    const std::vector<std::string> *payload; // pointer to email lines
    size_t lines_read = 0;                   // current line index
};

static size_t payload_source(void *ptr, size_t size, size_t nmemb, void *userp) {
    auto *upload_ctx = static_cast<UploadContext *>(userp);
    size_t buffer_size = size * nmemb;

    if (upload_ctx->lines_read >= upload_ctx->payload->size()) {
        return 0; // No more data
    }

    const std::string &line = (*upload_ctx->payload)[upload_ctx->lines_read++];
    size_t copy_size = line.size();

    if (copy_size > buffer_size) {
        // Should not happen with typical small lines
        copy_size = buffer_size;
    }
    memcpy(ptr, line.c_str(), copy_size);
    return copy_size;
}

int main() {
    // SMTP credentials and server info
    const std::string smtp_url = "smtp://smtp.gmail.com:587"; // change if needed
    const std::string username = "your_email@gmail.com";      // sender address / SMTP username
    const std::string password = "your_app_password";         // app password or SMTP password

    const std::string sender = "<your_email@gmail.com>";
    const std::string recipient = "<recipient@example.com>";
    const std::string subject = "Test email from C++ via libcurl";
    const std::string body =
        "Hello,\n\nThis is a test email sent from C++ using libcurl!\n";

    // Build the payload (headers + blank line + body). Each line must end with \r\n.
    std::vector<std::string> payload = {
        "Date: Mon, 29 Jan 2024 12:00:00 +0000\r\n",
        "To: " + recipient + "\r\n",
        "From: " + sender + "\r\n",
        "Subject: " + subject + "\r\n",
        "MIME-Version: 1.0\r\n",
        "Content-Type: text/plain; charset=UTF-8\r\n",
        "\r\n", // blank line separates headers from body
    };

    // Split body by \n to ensure proper CRLF termination
    size_t start = 0;
    while (true) {
        size_t end = body.find('\n', start);
        std::string line = body.substr(start, (end == std::string::npos ? end : end - start));
        payload.emplace_back(line + "\r\n");
        if (end == std::string::npos) {
            break;
        }
        start = end + 1;
    }

    CURL *curl = curl_easy_init();
    if (!curl) {
        std::cerr << "Failed to initialize libcurl" << std::endl;
        return 1;
    }

    UploadContext upload_ctx{&payload};

    struct curl_slist *recipients = nullptr;
    recipients = curl_slist_append(recipients, recipient.c_str());

    curl_easy_setopt(curl, CURLOPT_URL, smtp_url.c_str());
    curl_easy_setopt(curl, CURLOPT_USERNAME, username.c_str());
    curl_easy_setopt(curl, CURLOPT_PASSWORD, password.c_str());

    // Use STARTTLS if the server supports it (port 587)
    curl_easy_setopt(curl, CURLOPT_USE_SSL, CURLUSESSL_ALL);
    curl_easy_setopt(curl, CURLOPT_MAIL_FROM, sender.c_str());
    curl_easy_setopt(curl, CURLOPT_MAIL_RCPT, recipients);

    // Enable verbose output for debugging (optional)
    // curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

    // Pass payload via callback
    curl_easy_setopt(curl, CURLOPT_READFUNCTION, payload_source);
    curl_easy_setopt(curl, CURLOPT_READDATA, &upload_ctx);
    curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);

    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
    } else {
        std::cout << "Email sent successfully!" << std::endl;
    }

    // Clean up
    curl_slist_free_all(recipients);
    curl_easy_cleanup(curl);
    curl_global_cleanup();

    return (res == CURLE_OK) ? 0 : 1;
}