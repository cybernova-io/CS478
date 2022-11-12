import Layout from "../components/Layout";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";

Messages.title = "Screagles Connect: Messages";

export default function Messages() {
  return (
    <Layout>
      <Box
        sx={{
          width: "100%",
          margin: "auto",
          mt: 20,
          p: 2,
        }}
      >
        <Typography variant="h4" textAlign="center" gutterBottom>
          Select a message
        </Typography>
        <Typography
          variant="body2"
          textAlign="center"
          sx={{ color: "#808080" }}
        >
          Select from an existing conversation, or start a new one by adding
          friends.
        </Typography>
      </Box>
    </Layout>
  );
}
