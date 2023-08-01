import {useState, useRef} from 'react';
import AddIcon from '@mui/icons-material/Add';
import CloseIcon from '@mui/icons-material/Close';
// validate schema with joi

import {Resource} from '../../types/resources';

import {parseData} from './Controller';

import './ControlMenu.css';

type ControlMenuProps = {
  setResources: React.Dispatch<React.SetStateAction<Resource[]>>;
  setSortAttribute: React.Dispatch<React.SetStateAction<string>>;
};

const ControlMenu = ({setResources, setSortAttribute}: ControlMenuProps) => {
  const fileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

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

      <div className="menu-item">
        <div className="menu-item__header">
          <span>
            <img src="./icons/sort.png" alt="" />
          </span>
          <h3>Sort</h3>
        </div>
        <div className="menu-item__content">
          <div>
            <input
              type="radio"
              name="sort-type"
              id="sort-name"
              value="name"
              onChange={e => {
                setSortAttribute(e.target.value);
              }}
            />
            <label htmlFor="sort-name">Name</label>
          </div>

          <div>
            <input
              type="radio"
              name="sort-type"
              id="sort-date"
              defaultChecked
              value="date"
              onChange={e => {
                setSortAttribute(e.target.value);
              }}
            />
            <label htmlFor="sort-date">Creation Date</label>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ControlMenu;
