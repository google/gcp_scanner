import './ControlMenuLayout.css';

type ControlMenuLayoutProps = {
  children?: React.ReactNode;
};

const ControlMenuLayout = ({children}: ControlMenuLayoutProps) => {
  return <div className="control-menu">{children}</div>;
};

export default ControlMenuLayout;
