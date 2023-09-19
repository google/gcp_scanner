import {useState, useRef} from 'react';
import CloseIcon from '@mui/icons-material/Close';

import {Resource} from '../../../types/resources';
import {IAMRole} from '../../../types/IAMPolicy';
import {addFile, deleteFile} from '../Controller';

type UploadMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
  setRoles: React.Dispatch<React.SetStateAction<IAMRole[]>>;
  setProjects: React.Dispatch<React.SetStateAction<string[]>>;
  setAllowedProjects: React.Dispatch<React.SetStateAction<string[]>>;
};

type FileInfo = {
  name: string;
  projects: string[];
};

const UploadMenu = ({
  setResources,
  setRoles,
  setProjects,
  setAllowedProjects,
}: UploadMenuProps) => {
  const fileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<FileInfo[]>([]);
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

          if (!fileInput.current?.files) {
            setError('No file selected');
            return;
          }

          // loop throw files
          for (let i = 0; i < fileInput.current?.files?.length; i++) {
            const file = fileInput.current?.files?.[i];

            // check if file is already uploaded
            if (files.find(prevFile => prevFile.name === file.name)) {
              setError('File already uploaded');
              return;
            }

            addFile(
              file,
              setFiles,
              setResources,
              setRoles,
              setProjects,
              setAllowedProjects,
              setError
            );
          }
        }}
      >
        <input
          type="file"
          accept=".json"
          multiple
          ref={fileInput}
          onChange={() => {
            setError(null);
            // trigger submit
            fileInput.current?.form?.dispatchEvent(
              new Event('submit', {cancelable: true, bubbles: true})
            );
          }}
          className="add-input"
        />
      </form>
      {error && <p className="error">{error}</p>}
      {files.length > 0 && (
        <div className="files-list">
          {files.map(file => (
            <div className="file-item" key={file.name}>
              <p>{file.name}</p>
              <button
                className="remove-button"
                onClick={() => {
                  deleteFile(
                    file,
                    setFiles,
                    setResources,
                    setRoles,
                    setProjects
                  );
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
