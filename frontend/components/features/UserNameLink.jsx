import Link from "next/link";
import { Typography } from "@mui/material";

export default function UserNameLink(props) {
  return (
    <Link href={`/profile/${props.data._id}`} passHref>
      <Typography
        component="a"
        sx={{
          color: "inherit",
          cursor: "pointer",
          textDecoration: "none",
          "&:hover": {
            textDecoration: "underline",
          },
        }}
        variant="body2"
      >
        {`${props.data.firstName} ${props.data.lastName}`}
      </Typography>
    </Link>
  );
}
