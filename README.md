# Mediacontent broadcasting with analytics System Management API Documentation

## Overview

This API is developed using Django REST Framework and is designed for managing a video system including cameras, screens, media content, and schedules. The API includes various endpoints that allow performing CRUD operations as well as specialized functions for downloading media files and providing detailed information about the system.

## API Endpoints

### Cameras (`/api/camera/`)
- **GET**: Retrieve a list of all cameras.
- **POST**: Add a new camera.
- **GET `/api/camera/{id}/`**: Retrieve details of a specific camera.
- **PUT/PATCH `/api/camera/{id}/`**: Update details of a camera.
- **DELETE `/api/camera/{id}/`**: Remove a camera.

### Screens (`/api/screen/`)
- **GET**: Retrieve a list of all screens.
- **POST**: Add a new screen.
- **GET `/api/screen/{id}/`**: Retrieve details of a specific screen.
- **PUT/PATCH `/api/screen/{id}/`**: Update details of a screen.
- **DELETE `/api/screen/{id}/`**: Remove a screen.
- **GET `/api/screen/{id}/videomanager/{mode}/`**: Retrieve or download videomanager data for a screen depending on the mode (`show` or `download`).

### Camera-Screen Relations (`/api/camerascreen/`)
- CRUD operations to manage relations between cameras and screens.

### Schedules (`/api/schedule/`)
- CRUD operations to manage schedules of media content on screens.

### Media Content (`/api/mediacontent/`)
- **GET**: Retrieve a list of all media content.
- **POST**: Add media content using a specialized serializer for writing.
- **GET `/api/mediacontent/{id}/`**: Detailed information about media content.
- **PUT/PATCH `/api/mediacontent/{id}/`**: Update media content.
- **DELETE `/api/mediacontent/{id}/`**: Remove media content.
- **GET `/api/mediacontent/{id}/video/download/`**: Download video file.
- **GET `/api/mediacontent/{id}/preview/download/`**: Download preview file.

### Statistics (`/api/statistics/`)
- CRUD operations to manage statistical data on media viewing.

### Detailed Camera Service (`/api/camera-service-detail`)
- **GET**: Retrieve detailed information about all cameras, including associated screens, schedules, and media content.

## Media Files Management
For managing media files (video and images), a URL registration is provided through which access to files uploaded into the system can be achieved.

## Development and Settings
The API is built using Django and Django REST Framework. Data is stored using Django models connected to a database through configured tables. The models define fields and data types, which include text fields, file links, and relationships with other models.

## Integration and Extensions
The API facilitates easy integration with other systems and applications, providing flexible interfaces for working with video data and managing video equipment.