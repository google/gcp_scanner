import {useState, useRef} from 'react';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';

import {Resource} from '../../types/resources';
import {OutputFile} from '../../types/resources';

import {parseData} from './Controller';

import './ControlMenu.css';

type ControlMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
};

const ControlMenu = ({setResources}: ControlMenuProps) => {
  const fileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<string[]>([]);
  return (
    <div className="control-menu">
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
            const file = fileInput.current?.files?.[0];

            if (!file) return;
            // check if file is already uploaded
            if (files.includes(file.name)) return;
            const reader = new FileReader();
            reader.readAsText(file);
            reader.onload = e => {
              const result = e.target?.result as string;
              const data = JSON.parse(result) as OutputFile;

              const resources = parseData(data, file.name);

              setResources((prevResources: Resource[]) => [
                ...prevResources,
                ...resources,
              ]);
              setFiles([...files, file.name]);
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
    </div>
  );
};

export default ControlMenu;
