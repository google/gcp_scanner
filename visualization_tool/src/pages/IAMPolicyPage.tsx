import {IAMRole} from '../types/IAMPolicy';
import RolesList from '../components/RolesList/RolesList';

type IAMPolicyPageProps = {
  roles: IAMRole[];
  emailQuery: string;
  allowedProjects: string[];
};

const IAMPolicyPage = ({
  roles,
  emailQuery,
  allowedProjects,
}: IAMPolicyPageProps) => {
  return (
    <RolesList
      roles={roles}
      emailQuery={emailQuery}
      allowedProjects={allowedProjects}
    ></RolesList>
  );
};

export default IAMPolicyPage;
