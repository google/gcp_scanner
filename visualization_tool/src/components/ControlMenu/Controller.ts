import {
  OutputFile,
  Resource,
  ResourceType,
  availableResourceTypes,
} from '../../types/resources';

import {IAMRole, IMAPolicyField} from '../../types/IMAPolicy';

const titleCase = (str: string) => {
  return str
    .replace('_', ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
};

const parseData = (data: OutputFile, fileName: string) => {
  const resources = [];
  for (const [projectId, projectData] of Object.entries(data.projects)) {
    for (const [resourceType, resourceList] of Object.entries(projectData)) {
      let type = titleCase(resourceType.slice(0, -1));
      if (type === 'Dns Policie') type = 'Dns Policy';
      if (
        resourceList instanceof Array &&
        availableResourceTypes.includes(type as ResourceType)
      ) {
        const currentResources = [];
        for (const resource of resourceList) {
          const resourceData: Record<string, string | number> = {};
          resourceData['file'] = fileName;
          resourceData['projectId'] = projectId;

          for (const [key, value] of Object.entries(resource)) {
            switch (typeof value) {
              case 'string':
                // if this attribute is a link, get the last part of the link
                if (value.split('/').length > 1) {
                  resourceData[key] = value.split('/').at(-1) || 'unknown';
                } else {
                  resourceData[key] = value;
                }
                break;
              case 'number':
                resourceData[key] = value;
                break;
              default:
                break;
            }
          }

          resourceData['name'] = resourceData['name'] || 'unknown';
          resourceData['status'] = resourceData['status'] || 'READY';
          resourceData['type'] = type;

          currentResources.push(resourceData as Resource);
        }

        resources.push(...currentResources);
      }
    }
  }

  return resources;
};

const parseIAMData = (data: OutputFile, fileName: string) => {
  const roles: IAMRole[] = [];
  for (const [projectId, projectData] of Object.entries(data.projects)) {
    const currentRoles = projectData?.iam_policy as IMAPolicyField[];

    if (roles instanceof Array) {
      for (const role of currentRoles) {
        roles.push({
          file: fileName,
          projectId,
          role: `${projectId}__${role.role.split('/')[1]}`,
          members: role.members.map(member => {
            return {
              memberType: member.split(':')[0],
              email: member.split(':')[1],
            };
          }),
        });
      }
    }
  }

  // console.log(roles);
  return roles;
};
export {parseData, parseIAMData};
