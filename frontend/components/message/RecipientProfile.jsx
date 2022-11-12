import { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import { useRouter } from "next/router";
import Typography from "@mui/material/Typography";
import userService from "../../src/features/users/usersService";
import Avatar from "@mui/material/Avatar";
import Stack from "@mui/material/Stack";
import Skeleton from "@mui/material/Skeleton";

export default function RecipientProfile() {
  const router = useRouter();
  const { user } = useSelector((state) => state.auth);
  const { id } = router.query;
  const [recipientData, setRecipientData] = useState([]);

  // Get recipient data
  const getRecipientData = async () => {
    var userData = await userService.getUserDataById(id, user.token);
    userData = {
      _id: userData._id,
      lastName: userData.lastName,
      firstName: userData.firstName,
      photo: userData.photo,
    };
    setRecipientData(userData);
  };

  useEffect(() => {
    id && getRecipientData();
  }, [id]);

  return (
    <Stack
      direction="row"
      spacing={2}
      justifyContent="flex-start"
      alignItems="center"
    >
      {recipientData.length === 0 ? (
        <>
          <Skeleton
            variant="circular"
            width={40}
            height={40}
            animation="wave"
          />
          <Skeleton animation="wave" width="25%" />
        </>
      ) : (
        <>
          <Avatar
            src={recipientData.photo && `/uploads/${recipientData.photo}`}
            aria-label="avatar"
          />
          <Typography variant="body2">
            {`${recipientData.firstName} ${recipientData.lastName}`}
          </Typography>
        </>
      )}
    </Stack>
  );
}
