type SortMenuProps = {
  setSortAttribute: React.Dispatch<React.SetStateAction<string>>;
};

const SortMenu = ({setSortAttribute}: SortMenuProps) => {
  return (
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
  );
};

export default SortMenu;
