import {useState, useRef} from 'react';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';

import {Resource} from '../../../types/resources';
import {IAMRole} from '../../../types/IMAPolicy';
import {parseData, parseIAMData} from '../Controller';

type UploadMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
  setRoles: React.Dispatch<React.SetStateAction<IAMRole[]>>;
};

const UploadMenu = ({setResources, setRoles}: UploadMenuProps) => {
  const fileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);
  return (
    <div className="menu-item">
      <div className="menu-item__header">
        <span>
          <img src="./icons/upload.png" alt="" />
        </span>
        <h3>Upload</h3>
      </div>
      <form
        className="upload-form"
        onSubmit={e => {
          e.preventDefault();
          setError(null);
          const file = fileInput.current?.files?.[0];

          if (!file) {
            setError('No file selected');
            return;
          }
          // check if file is already uploaded
          if (files.includes(file.name)) {
            setError('File already uploaded');
            return;
          }

          const reader = new FileReader();
          reader.readAsText(file);
          reader.onload = e => {
            const result = e.target?.result as string;

            try {
              const data = JSON.parse(result);
              const resources = parseData(data, file.name);
              setResources((prevResources: Resource[]) => [
                ...prevResources,
                ...resources,
              ]);

              const roles = parseIAMData(data, file.name);
              setRoles((prevRoles: IAMRole[]) => [...prevRoles, ...roles]);

              setFiles([...files, file.name]);
            } catch (err) {
              setError('Invalid file');
              return;
            }
          };
        }}
      >
        <input
          type="file"
          name=""
          id=""
          accept=".json"
          ref={fileInput}
          className="add-input"
        />
        <button type="submit" className="add-button">
          <AddIcon
            sx={{
              fontSize: '2rem',
              color: '#4285F4',
            }}
          />
        </button>
      </form>
      {error && <p className="error">{error}</p>}
      {files.length > 0 && (
        <div className="files-list">
          {files.map(file => (
            <div className="file-item" key={file}>
              <p>{file}</p>
              <button
                className="remove-button"
                onClick={() => {
                  setFiles(prevFiles => {
                    return prevFiles.filter(prevFile => prevFile !== file);
                  });
                  setResources(prevResources => {
                    return prevResources.filter(
                      prevResource => prevResource.file !== file
                    );
                  });
                  setRoles(prevRoles => {
                    return prevRoles.filter(prevRole => prevRole.file !== file);
                  });
                }}
              >
                <CloseIcon
                  sx={{
                    fontSize: '20px',
                    color: '#505050',
                    hover: {
                      color: '#4285F4',
                    },
                  }}
                />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default UploadMenu;
