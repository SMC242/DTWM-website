import React, { FC, useState, useEffect } from "react";
import {
  Box,
  useColorModeValue,
  HStack,
  VStack,
  Slide,
  BoxProps,
  Divider,
} from "@chakra-ui/react";
import ModeButton from "../inputs/mode_btn";
import Link from "next/link";

type ScrollEvent = { scrollX: number; scrollY: number };
export type LinkType = { text: string; route: string };

export interface NavBarProps {
  links: Array<LinkType>;
}

interface NavItemProps extends LinkType {
  width?: string;
}

const NavItemBox: FC<BoxProps> = (props) => (
  <Box h="100%" d="inline" mx="2" {...props}>
    {props.children}
  </Box>
);

const NavItem: FC<NavItemProps> = ({ text, route, width }) => (
  <NavItemBox w={width}>
    <Link href={route} passHref>
      <a>{text}</a>
    </Link>
  </NavItemBox>
);

export const HNavbar: FC<NavBarProps> = ({ links }) => {
  const bg = useColorModeValue("yellow.500", "blue.800");
  const [revealed, set_revealed] = useState(true);
  // Hide the menu unless at the top or bottom of the page
  const handle_scroll = () => {
    // How many pixels around the top and bottom to show the navbar for
    const TOLERANCE = 100;
    const current_position = window.pageYOffset;
    const max_position = document.body.scrollHeight - window.innerHeight;
    const below_top = current_position > TOLERANCE;
    const at_bottom = current_position >= max_position - TOLERANCE;
    if (below_top && !at_bottom) return set_revealed(false);
    set_revealed(true);
  };
  useEffect(() => {
    document.addEventListener("scroll", handle_scroll);
    return () => document.removeEventListener("scroll", handle_scroll);
  });

  return (
    <Box marginBottom="3rem">
      <Slide direction="top" in={revealed}>
        <Box bg={bg} w="100%" transition="height">
          <HStack>
            {links.map((l, i) => (
              <NavItem {...l} key={i} />
            ))}
            <NavItemBox>
              <ModeButton />
            </NavItemBox>
          </HStack>
        </Box>
      </Slide>
    </Box>
  );
};
