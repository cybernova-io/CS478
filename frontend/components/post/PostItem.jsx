import * as React from "react";
import { useState, useEffect } from "react";
import { styled } from "@mui/material/styles";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Collapse from "@mui/material/Collapse";
import Avatar from "@mui/material/Avatar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import { red } from "@mui/material/colors";
import FavoriteIcon from "@mui/icons-material/Favorite";
import ShareIcon from "@mui/icons-material/Share";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import MoreVertIcon from "@mui/icons-material/MoreVert";
import Grid from "@mui/material/Grid";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import ListItemText from "@mui/material/ListItemText";
import ListItemIcon from "@mui/material/ListItemIcon";
import EditPostForm from "./EditPostForm";
import { useDispatch } from "react-redux";
import DeleteDialog from "../alert-box/DeleteDialog";

const ExpandMore = styled((props) => {
  const { expand, ...other } = props;
  return <IconButton {...other} />;
})(({ theme, expand }) => ({
  transform: !expand ? "rotate(0deg)" : "rotate(180deg)",
  marginLeft: "auto",
  transition: theme.transitions.create("transform", {
    duration: theme.transitions.duration.shortest,
  }),
}));

export default function PostItem({ post }) {
  const dispatch = useDispatch();

  const [deleteDialog, setdeleteDialog] = React.useState(false);

  var date = new Date(post.createdAt);

  const month = date.toLocaleString("default", { month: "long" });

  var newdate = `${month}  ${date.getDate()}, ${date.getFullYear()}`;

  const [expanded, setExpanded] = React.useState(false);

  const [editPostForm, setEditPostForm] = React.useState(false);

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };

  const [anchorEl, setAnchorEl] = React.useState(null);

  const openOptions = Boolean(anchorEl);

  const handleClickOptions = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleCloseOptions = () => {
    setAnchorEl(null);
  };

  const toggleEditPostModal = () => {
    setEditPostForm((prevData) => !prevData);
  };

  const handleDeleteDialog = () => {
    setdeleteDialog((prevData) => !prevData);
  };

  const ReadMore = ({ children }) => {
    const text = children;
    const [isReadMore, setIsReadMore] = useState(true);
    const toggleReadMore = () => {
      setIsReadMore(!isReadMore);
    };
    return (
      <Typography
        variant="body2"
        color="text.secondary"
        sx={{ whiteSpace: "pre-line" }}
      >
        {isReadMore ? text.slice(0, 40) : text}
        <br />
        <span
          onClick={toggleReadMore}
          className="read-or-hide"
          style={{ color: "#1976d2", cursor: "pointer" }}
        >
          {isReadMore && text.length > 40 ? "...read more" : ""}
        </span>
      </Typography>
    );
  };

  return (
    <Grid item xs={12} sm={6} md={12}>
      <Card
        sx={{
          display: "flex",
          flexDirection: "column",
          maxWidth: 700,
          margin: "auto",
        }}
      >
        <CardHeader
          avatar={
            <Avatar sx={{ bgcolor: red[500] }} aria-label="avatar">
              R
            </Avatar>
          }
          action={
            <>
              <IconButton
                aria-label="more"
                id="long-button"
                aria-controls={openOptions ? "long-menu" : undefined}
                aria-expanded={openOptions ? "true" : undefined}
                aria-haspopup="true"
                onClick={handleClickOptions}
              >
                <MoreVertIcon />
              </IconButton>
              <Menu
                id="long-menu"
                MenuListProps={{
                  "aria-labelledby": "menu-button",
                }}
                anchorEl={anchorEl}
                open={openOptions}
                onClose={handleCloseOptions}
                PaperProps={{
                  style: {
                    width: "20ch",
                  },
                }}
              >
                <MenuItem onClick={toggleEditPostModal}>
                  <ListItemIcon>
                    <EditIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Edit</ListItemText>
                </MenuItem>
                <EditPostForm
                  key={post._id}
                  editPostForm={editPostForm}
                  toggleEditPostModal={toggleEditPostModal}
                  postData={post}
                />
                <MenuItem onClick={handleDeleteDialog}>
                  <ListItemIcon>
                    <DeleteIcon fontSize="small" />
                  </ListItemIcon>
                  <ListItemText>Delete</ListItemText>
                </MenuItem>
                <DeleteDialog
                  deleteDialog={deleteDialog}
                  postData={post}
                  handleDeleteDialog={handleDeleteDialog}
                />
              </Menu>
            </>
          }
          title="Shrimp and Chorizo Paella"
          subheader={newdate}
        />
        <CardContent>
          <ReadMore>{post.text}</ReadMore>
        </CardContent>
        {post.photo && (
          <CardMedia
            component="img"
            image={`/uploads/${post.photo}`}
            alt={post.photo}
          />
        )}
        <CardActions disableSpacing>
          <IconButton aria-label="add to favorites">
            <FavoriteIcon />
          </IconButton>
          <IconButton aria-label="share">
            <ShareIcon />
          </IconButton>
          <ExpandMore
            expand={expanded}
            onClick={handleExpandClick}
            aria-expanded={expanded}
            aria-label="show more"
          >
            <ExpandMoreIcon />
          </ExpandMore>
        </CardActions>
        <Collapse in={expanded} timeout="auto" unmountOnExit>
          <CardContent>
            <Typography paragraph>Method:</Typography>
            <Typography paragraph>
              Heat 1/2 cup of the broth in a pot until simmering, add saffron
              and set aside for 10 minutes.
            </Typography>
            <Typography paragraph>
              Heat oil in a (14- to 16-inch) paella pan or a large, deep skillet
              over medium-high heat. Add chicken, shrimp and chorizo, and cook,
              stirring occasionally until lightly browned, 6 to 8 minutes.
              Transfer shrimp to a large plate and set aside, leaving chicken
              and chorizo in the pan. Add pimentón, bay leaves, garlic,
              tomatoes, onion, salt and pepper, and cook, stirring often until
              thickened and fragrant, about 10 minutes. Add saffron broth and
              remaining 4 1/2 cups chicken broth; bring to a boil.
            </Typography>
            <Typography paragraph>
              Add rice and stir very gently to distribute. Top with artichokes
              and peppers, and cook without stirring, until most of the liquid
              is absorbed, 15 to 18 minutes. Reduce heat to medium-low, add
              reserved shrimp and mussels, tucking them down into the rice, and
              cook again without stirring, until mussels have opened and rice is
              just tender, 5 to 7 minutes more. (Discard any mussels that
              don&apos;t open.)
            </Typography>
            <Typography>
              Set aside off of the heat to let rest for 10 minutes, and then
              serve.
            </Typography>
          </CardContent>
        </Collapse>
      </Card>
    </Grid>
  );
}
