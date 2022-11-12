import * as React from "react";
import { useEffect } from "react";
import PropTypes from "prop-types";
import Box from "@mui/material/Box";
import { styled } from "@mui/material/styles";
import { Typography } from "@mui/material";
import Drawer from "@mui/material/Drawer";
import MuiDrawer from "@mui/material/Drawer";
import Grid from "@mui/material/Grid";
import { useRouter } from "next/router";
import FriendRequests from "../components/friends/FriendRequests";
import FriendSuggestions from "../components/friends/FriendSuggestions";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Divider from "@mui/material/Divider";
import DrawerMenu from "../components/drawer/DrawerMenu";
import MessageUserList from "../components/message/MessageUserList";
import RecipientProfile from "../components/message/RecipientProfile";
import Stack from "@mui/material/Stack";
import Link from "next/link";

const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: "hidden",
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create("width", {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: "hidden",
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up("sm")]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const CustomDrawer = styled(MuiDrawer, {
  shouldForwardProp: (prop) => prop !== "open",
})(({ theme, open }) => ({
  width: drawerWidth,
  height: "100%",
  flexShrink: 0,
  whiteSpace: "nowrap",
  boxSizing: "border-box",
  marginLeft: "auto",
  ...(open && {
    ...openedMixin(theme),
    "& .MuiDrawer-paper": openedMixin(theme),
  }),
  ...(!open && {
    ...closedMixin(theme),
    "& .MuiDrawer-paper": closedMixin(theme),
  }),
}));

function ResponsiveDrawer(props) {
  const router = useRouter();

  var localIsDarkMode = JSON.parse(localStorage.getItem("isDarkMode"));

  const [mobileOpen, setMobileOpen] = React.useState(false);

  const [open, setOpen] = React.useState(
    window.innerWidth >= 1281 || window.innerWidth <= 599 ? true : false
  );

  const [containerWidth, setContainerWidth] = React.useState(
    window.innerWidth <= 899 ? false : true
  );

  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const firstPath = router.pathname.split("/")[1];

  var pageTitle = firstPath;

  useEffect(() => {
    function watchWidth() {
      if (window.innerWidth >= 1200 || window.innerWidth <= 599) {
        setOpen(true);
      } else if (window.innerWidth <= 1199) {
        setOpen(false);
      }

      window.innerWidth <= 899
        ? setContainerWidth(false)
        : setContainerWidth(true);
    }

    window.addEventListener("resize", watchWidth);

    return function () {
      window.removeEventListener("resize", watchWidth);
    };
  }, []);

  const { windowProps } = props;

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };
  const container =
    windowProps !== undefined ? () => window().document.body : undefined;

  return (
    <Box sx={{ display: "flex", flexDirection: "row", height: "100vh" }}>
      <Box
        component="nav"
        sx={{ flexGrow: 1, display: { xs: "none", sm: "block" } }}
      >
        {/* Desktop Drawer */}
        <CustomDrawer
          variant="permanent"
          sx={{
            display: { xs: "none", sm: "block" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              position: "static",
              backgroundColor: "inherit",
              pr: 2,
              pt: 2,
            },
            width: drawerWidth,
            height: "100%",
            marginLeft: "auto",
          }}
          open={open}
        >
          <Link href="/home" passHref>
            <Box component="a" sx={{ display: { lg: "none" } }}>
              <img
                src={`/logos/eagle5.png`}
                loading="lazy"
                style={{ width: "100%" }}
              />
            </Box>
          </Link>
          <Link href="/home" passHref>
            <Box component="a" sx={{ display: { xs: "none", lg: "block" } }}>
              <img
                src={
                  localIsDarkMode
                    ? `/logos/southindscreagles.png`
                    : `/logos/southindscreagles.png`
                }
                loading="lazy"
                style={{ width: "100%" }}
              />
            </Box>
          </Link>

          <DrawerMenu open={open} />
        </CustomDrawer>
      </Box>

      {/* Mobile Drawer */}
      <Box
        component="nav"
        sx={{
          width: { sm: drawerWidth },
          flexShrink: { sm: 0 },
          display: { xs: "block", sm: "none" },
        }}
      >
        <Drawer
          container={container}
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: "block", sm: "none" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
              pt: 2,
            },
          }}
        >
          <Link href="/home" passHref>
            <Box component="a" sx={{ pl: 2 }}>
              <img
                src={
                  localIsDarkMode
                    ? `/logos/southindscreagles.png`
                    : `/logos/southindscreagles.png`
                }
                loading="lazy"
                style={{ width: "90%" }}
              />
            </Box>
          </Link>
          <DrawerMenu open={open} />
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          overflow: "auto",
        }}
      >
        <Box
          sx={{
            display: "flex",
            width: containerWidth ? "950px" : "auto",
          }}
        >
          <Grid container>
            {/* Show in messages page */}
            <MessageUserList handleDrawerToggle={handleDrawerToggle} />
            <Grid item xs={router.pathname === "/messages" ? 8 : 12} md={8}>
              <Box>
                <Box
                  sx={{
                    width: "100%",
                    p: 2,
                    py: 1.5,
                    zIndex: 99,
                    position: "sticky",
                    top: "0px",
                    backdropFilter: "blur(12px)",
                  }}
                >
                  <Stack direction="row">
                    <Typography variant="h6">
                      <IconButton
                        color="inherit"
                        aria-label="open drawer"
                        edge="start"
                        onClick={handleDrawerToggle}
                        sx={{ mr: 2, display: { sm: "none" } }}
                      >
                        <MenuIcon />
                      </IconButton>
                      {router.pathname !== "/messages" &&
                        router.pathname !== "/messages/[id]" &&
                        capitalizeFirstLetter(pageTitle)}
                      {router.pathname === "/saved" && " Post"}
                    </Typography>

                    {router.pathname === "/messages/[id]" && (
                      <RecipientProfile />
                    )}
                  </Stack>
                </Box>
                <Grid container spacing={2} sx={{ p: "16px" }}>
                  {props.content}
                </Grid>
              </Box>
            </Grid>
            {router.pathname !== "/messages" &&
              router.pathname !== "/messages/[id]" && (
                <Grid
                  item
                  xs={4}
                  sx={{ display: { xs: "none", sm: "none", md: "block" } }}
                >
                  <Box
                    sx={{
                      width: "100%",
                      p: 2,
                      zIndex: 99,
                      position: "sticky",
                      top: "0px",
                      boxSizing: "border-box",
                      backgroundColor: "inherit",
                      borderLeft: "1px solid",
                      borderColor: localIsDarkMode
                        ? "rgba(255, 255, 255, 0.12)"
                        : "rgba(0, 0, 0, 0.12)",
                      position: "sticky",
                      top: "0px",
                      height: "100vh",
                    }}
                  >
                    <FriendRequests />
                    <Divider sx={{ my: 2 }} />
                    <FriendSuggestions />
                  </Box>
                </Grid>
              )}
          </Grid>
        </Box>
      </Box>
    </Box>
  );
}

ResponsiveDrawer.propTypes = {
  /**
   * Injected by the documentation to work in an iframe.
   * You won't need it on your project.
   */
  window: PropTypes.func,
};

export default ResponsiveDrawer;
