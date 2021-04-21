import React, { FC, useState } from "react";
import {
  Box,
  useColorModeValue,
  HStack,
  VStack,
  Slide,
  BoxProps,
  Grid,
  useStyleConfig,
} from "@chakra-ui/react";
import ModeButton from "../inputs/mode_btn";
import Link from "next/link";
import with_scroll_cbs from "../wrappers/scroll";

export type LinkType = { text: string; route: string };

export interface NavBarProps {
  links: Array<LinkType>;
}

interface NavItemProps extends LinkType {}

const NavItemBox: FC<BoxProps> = (props) => {
  const styles = useStyleConfig("NavItemBox");
  return (
    <Box sx={styles} {...props}>
      {props.children}
    </Box>
  );
};

const NavItem: FC<NavItemProps> = ({ text, route }) => (
  <NavItemBox>
    <Link href={route} passHref>
      <a>{text}</a>
    </Link>
  </NavItemBox>
);

const Inner: FC<NavBarProps & { revealed: boolean }> = ({
  links,
  revealed,
}) => {
  return (
    <Box sx={useStyleConfig("NavbarContainer")}>
      <Slide direction="top" in={revealed}>
        <Box sx={useStyleConfig("NavbarBG")}>
          <Grid
            templateColumns="repeat(2, 2fr)"
            gap={300}
            sx={useStyleConfig("NavbarGrid")}
          >
            <HStack sx={useStyleConfig("NavbarStack")}>
              {links.map((l, i) => (
                <NavItem {...l} key={i} />
              ))}
            </HStack>
            <NavItemBox textAlign="right">
              <ModeButton />
            </NavItemBox>
          </Grid>
        </Box>
      </Slide>
    </Box>
  );
};

export const HNavbar: FC<NavBarProps> = (props) => {
  const [revealed, set_revealed] = useState(true);
  const Wrapped = with_scroll_cbs(
    Inner,
    () => set_revealed(true),
    () => set_revealed(false)
  );

  return <Wrapped revealed={revealed} {...props} />;
};
