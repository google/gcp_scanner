# Technical Documentation For GCP Scanner Visualizer

## Table of Contents

- [Introduction](#introduction)
- [Table of Contents](#table-of-contents)
- [Architecture Overview](#architecture-overview)
  - [Types Definition](#types-definition)
  - [Parsing Logic](#parsing)
  - [UI](#ui)
- [Deployment](#deployment)

## Introduction

This document describes the architecture of the GCP Scanner Visualizer and how it integrates with the GCP scanner package.

## Architecture Overview

The main goal of this application is to help the users visualize the GCP scanner results in a user-friendly way while also providing the ability to filter and search the results based on their needs. The app should also integrate easily with the GCP scanner package and add little to no new dependencies.

A reasonable choice is to develop the visualization tool as a single-page web application. This way, it's easy to run on any modern web browser. It also makes it easy to integrate with the GCP scanner package as it only adds a static HTML and JavaScript file to the GCP scanner package.

We can divide the architecture of the application into three parts:

- Types: The types definitions for objects used in the application.
- Parsing: The logic for parsing and extracting the data from the GCP Scanner.
- UI: The code and components hierarchy for displaying the data in the UI.

### Types Definition

The types layer contains the types definitions that used across the app. It works as a middle layer between the parsing layer and the UI layer Where it defines what data shape is expected from the parsing logic.

There are two main types of data that is extracted from the GCP Scanner:

- `Resources`: The resources that the credentials have access to.
- `IAM Policies`: The IAM policies roles that are attached to the projects found in the scan.

The resources related types are defined in the `types/resources.ts` file as follows:

- `Resource Type`: The type of the resource (e.g. `Compute Instance`, `Cloud Storage Bucket`, etc.).
- `ResourceStatus`: The status of the resource (e.g. `ACTIVE`, `DELETED`, etc.).
- `Resource`: The resource object that contains the fields that must exist in any resource which are:
  - `projectId`: The ID of the project that the resource belongs to.
  - `file`: The file that the resource was found in, as the visualizer can be used to visualize multiple GCP scanner output files.
  - `id`: The ID of the resource.
  - `name`: The name of the resource.
  - `type`: The type of the resource.
  - `creationTimestamp`: The creation time of the resource.
  - `status`: The status of the resource.

The IAM policies related types are defined in the `types/IAMPolicy.ts` file as follows:

- `Member`: The member object that contains the fields that must exist in any member which are:

  - `type`: The type of the member (e.g. `user`, `serviceAccount`, etc.).
  - `email`: The email of the member.

- `IAMPolicy`: The IAM policy object that contains the fields that must exist in any IAM policy which are:
  - `role`: The name of role for this policy.
  - `members`: The members of this policy.
  - `projectId`: The ID of the project that the IAM policy belongs to.
  - `file`: The file that the IAM policy was found in.

The `types/resources.ts` file also contains types related to the structure of the GCP scanner output file which are:

- `OutputFile`: The GCP scanner output file object schema.

### Parsing

The logic for parsing and extracting the data from the GCP Scanner output files is defined in the `components/ControlMenu/Controller.ts` file. and it contains two main functions:

- `parseResources`: This function extracts the resources from the GCP scanner output file. It takes in the `OutputFile` object and returns an array of `Resource` objects.
- `parseIAMRoles`: This function extracts the IAM policies from the GCP scanner output file. It takes in the `OutputFile` object and returns an array of `IAMPolicy` objects.

#### Parsing Resources

The logic for parsing the resources can be summarized as follows:

```
for each key in the project keys:
  if the key is a resource:
    parse the resources in the array and add them to the resources array
```

To extract the resources from the GCP scanner output file, We are looping through each key in the project keys. If the key is a resource, we are parsing the resource and adding it to the resources array.

To check if the key is a resource, we are checking it is in the `availableResourceTypes` array that is defined in the `types/resources.ts` file. The `availableResourceTypes` array contains the types of resources that we want to extract from the GCP scanner output file. These are the types of resources that are well tested and supported by the visualizer.

For parsing the resources, we are extracting all fields of type `string` and `number` from the resource object and then adding them to the resource object. We are also adding the `projectId` and `file` fields to the resource object.

#### Parsing IAM Policies

Same as the resources, looping through roles in the `iam_policy` key. For each role, we are looping through the members and adding them to the members array. Then we are adding the `projectId` and `file` fields to the IAM policy object and adding it to the IAM policies array.

### UI

The UI of the application is built using React and Material-UI. It has three main components:

- `Navbar`: The navbar component contains the navigation links for the app's different views and the search bar.
- `Control Menu`: The left side menu contains the upload menu that allows the user to upload GCP scanner output files and the filter and sort menus that allow the user to filter the resources and IAM policies based on their needs.
- `Content Area`: Main content of each view.

Currently, there are two views in the app:

- `Resources View`: This view displays the resources as cards in a grid. Each card contains the resource name, type, and status. The user can see more details about the resource by clicking on the details button on the card. The user can also filter and sort the resources based on their needs.

- `IAM Policies View`: This view displays the IAM policies in a table. The policies are grouped by the project ID. The user can see all members of a policy by clicking on the expand button in the policy row. The user can also filter the IAM policies based on their needs.

## Deployment

The visualizer is deployed as a static website that ships with the GCP scanner package and is served using the `http.server` module in Python. The `src/gui/app.py` python script is responsible for serving the visualizer static files that should be in the `src/gui/static` folder.

### Integration with GCP Scanner

The `npm run build` command in configured in the `package.json` file to build the visualizer and output the static files in the `src/gui/static` folder and the `MANIFEST.in` file is configured to include the static files in the `src/gui/static` folder in the GCP scanner package.

We also modified the `python-publish.yml` GitHub action workflow to build the visualizer and include the static files in the GCP scanner package when publishing to PyPI.

### Running the visualizer

The user can run the visualizer by running the following command:

```
gcp-scanner-visualizer -port <port>
```

The visualizer by default runs on port `8080` if no port is specified.
