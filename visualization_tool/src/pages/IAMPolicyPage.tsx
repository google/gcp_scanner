import {IAMRole} from '../types/IAMPolicy';
import RolesList from '../components/RolesList/RolesList';

type IAMPolicyPageProps = {
  roles: IAMRole[];
  emailQuery: string;
};

const IAMPolicyPage = ({roles, emailQuery}: IAMPolicyPageProps) => {
  return <RolesList roles={roles} emailQuery={emailQuery}></RolesList>;
};

export default IAMPolicyPage;
