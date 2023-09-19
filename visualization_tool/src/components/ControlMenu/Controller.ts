import {Resource, OutputFile} from '../../types/resources';
import {IAMRole} from '../../types/IAMPolicy';

import {parseResources, parseIAMRoles} from '../../parser/parser';

type FileInfo = {
  name: string;
  projects: string[];
};

const deleteFile = (
  file: FileInfo,
  setFiles: React.Dispatch<React.SetStateAction<FileInfo[]>>,
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>,
  setRoles: React.Dispatch<React.SetStateAction<IAMRole[]>>,
  setProjects: React.Dispatch<React.SetStateAction<string[]>>
) => {
  setFiles(prevFiles => {
    return prevFiles.filter(prevFile => prevFile.name !== file.name);
  });

  setProjects(prevProjects => {
    return prevProjects.filter(
      prevProject => !file.projects.includes(prevProject)
    );
  });

  setResources(prevResources => {
    return prevResources.filter(
      prevResource => prevResource.file !== file.name
    );
  });
  setRoles(prevRoles => {
    return prevRoles.filter(prevRole => prevRole.file !== file.name);
  });
};

const addFile = (
  file: File,
  setFiles: React.Dispatch<React.SetStateAction<FileInfo[]>>,
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>,
  setRoles: React.Dispatch<React.SetStateAction<IAMRole[]>>,
  setProjects: React.Dispatch<React.SetStateAction<string[]>>,
  setAllowedProjects: React.Dispatch<React.SetStateAction<string[]>>,
  setError: React.Dispatch<React.SetStateAction<string | null>>
) => {
  const reader = new FileReader();
  reader.readAsText(file);
  reader.onload = e => {
    const result = e.target?.result as string;

    try {
      const data = JSON.parse(result) as OutputFile;
      setProjects(prevProjects => [
        ...prevProjects,
        data.project_info.projectId,
      ]);
      setAllowedProjects(prevProjects => [
        ...prevProjects,
        data.project_info.projectId,
      ]);
      const resources = parseResources(data, file.name);
      setResources(prevResources => [...prevResources, ...resources]);

      const roles = parseIAMRoles(data, file.name);
      setRoles(prevRoles => [...prevRoles, ...roles]);

      setFiles(prevFiles => [
        ...prevFiles,
        {name: file.name, projects: [data.project_info.projectId]},
      ]);
    } catch (err) {
      console.log(err);
      console.log('Invalid file');
      setError('Invalid file');
      return;
    }
  };
};

export {deleteFile, addFile};
