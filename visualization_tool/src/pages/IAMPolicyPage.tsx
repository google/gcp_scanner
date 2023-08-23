import {IAMRole} from '../types/IMAPolicy';
import RolesList from '../components/RolesList/RolesList';

type IAMPolicyPageProps = {
  roles: IAMRole[];
};

const IAMPolicyPage = ({roles}: IAMPolicyPageProps) => {
  return <RolesList roles={roles}></RolesList>;
};

export default IAMPolicyPage;
