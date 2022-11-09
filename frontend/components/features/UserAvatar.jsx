import Avatar from "@mui/material/Avatar";
import { useSelector } from "react-redux";

export default function UserAvatar() {
  const { user } = useSelector((state) => state.auth);

  return <Avatar src={user.photo && `/uploads/${user.photo}`} />;
}
