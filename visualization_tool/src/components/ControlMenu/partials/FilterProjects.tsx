type FilterProjectsProps = {
  projects: string[];
  setAllowedProjects: React.Dispatch<React.SetStateAction<string[]>>;
};

const FilterProjects = ({
  projects,
  setAllowedProjects,
}: FilterProjectsProps) => {
  return (
    <div className="menu-item">
      <div className="menu-item__header">
        <span>
          <img src="./icons/filter.png" alt="" />
        </span>
        <h3>Projects</h3>
      </div>
      {projects.length > 0 && (
        <div className="menu-item__content">
          {projects.map(project => {
            return (
              <div key={project}>
                <input
                  type="checkbox"
                  name="resource-type"
                  id={project}
                  defaultChecked
                  onChange={e => {
                    if (e.target.checked) {
                      setAllowedProjects(prevProjects => [
                        ...prevProjects,
                        project,
                      ]);
                    } else {
                      setAllowedProjects(prevProjects => {
                        return prevProjects.filter(
                          prevProject => prevProject !== project
                        );
                      });
                    }
                  }}
                />
                <label htmlFor={project}>{project}</label>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default FilterProjects;
