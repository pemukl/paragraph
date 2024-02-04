# Paragraph
 A live version of the project is available at [paragraph.shnei.de](https://paragraph.shnei.de/DE/eWpG).
## Introduction
Paragraph is a hobby project designed to assist lawyers in navigating German legislation more efficiently. It addresses a gap in the current legal resources available at [gesetze-im-internet.de](https://gesetze-im-internet.de) by providing an interface with clickable references between laws, eliminating the need for manual searches.

## Project Components
The project pipeline comprises three main components:
1. **Scraping Legislation:** Automated scraping of [gesetze-im-internet.de](https://gesetze-im-internet.de) to gather the text of laws.
2. **Linking References:** Utilizing a combination of regex and API calls to OpenAI to identify and link references within the laws.
3. **Frontend Display:** A Svelte-based frontend that presents the laws in a user-friendly format, accessible via [paragraph.shnei.de](https://paragraph.shnei.de/).

Both the backend and frontend are included in this mono-repository, each with its own dedicated README for more detailed information.

## Setup and Installation
To get started with Paragraph, you will need Docker installed on your system. The project comes with a Docker Compose file for easy setup. Simply clone the repository, configure your `.env` file based on the provided example, and use Docker Compose to build and run the application.

## Technology Stack
- **Backend:** Python with regex and OpenAI for processing and linking law references. A Pydantic model ensures consistency.
- **Database:** MongoDB for storing linked laws and ensuring quick retrieval.
- **Frontend:** Svelte for a responsive and interactive user interface.

## Usage
Once the application is running and the laws are scraped, users can navigate through German laws.

## Feedback
Feel free to hit me up for any feedback or ideas.
