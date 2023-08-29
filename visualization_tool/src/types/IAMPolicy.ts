type Member = {
  memberType: string;
  email: string;
};

type IAMRole = {
  role: string;
  members: Member[];
  projectId: string;
  file: string;
};

type IMAPolicyField = {
  role: string;
  members: string[];
};

export type {Member, IAMRole, IMAPolicyField};
