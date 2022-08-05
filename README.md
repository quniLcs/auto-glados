# Auto-GLaDOS

## Update

This repo failed to work on August 4th, 2022 because of the version problem of Google Chrome, and the bug was fixed the next day. One can `fetch upstream` to update one's own repo.

## Installation

1. Get one's cookie by first logging in [GLaDOS](https://glados.rocks/), then opening the developer tools through any one of the following methods, reloading the page, and finally following `Network`, `console`, `Request Headers`, and `cookie`. Methods to open the developer tools:

   - Press [F12];
   - Right-click any blank space of the page and click `Inspect`;
   - Follow `Setting and others`, `More Tools` and `Developer Tools`.

2. Get one's [PushPlus](https://www.pushplus.plus/) token.

3. Fork this repo, and then in one's own repo, follow `Setting`, `Secrets`, `Actions` to create 2 new secrets, which will be kept confidential by GitHub.

   | Number | Name             | Value                |
   | ------ | ---------------- | -------------------- |
   | 1      | `GLADOS_COOKIE`  | One's GLaDOS Cookie  |
   | 2      | `PUSHPLUS_TOKEN` | One's PushPlus Token |

4. Then GitHub Action will help one to check in GLaDOS at 10 a.m. every day.