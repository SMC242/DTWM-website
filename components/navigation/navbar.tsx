import React, { FC, useState } from "react";
import {
  Box,
  useColorModeValue,
  HStack,
  VStack,
  Slide,
  BoxProps,
} from "@chakra-ui/react";
import ModeButton from "../inputs/mode_btn";
import Link from "next/link";
import with_scroll_cbs from "../wrappers/scroll";

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

const Inner: FC<NavBarProps & { revealed: boolean }> = ({
  links,
  revealed,
}) => {
  const bg = useColorModeValue("yellow.500", "blue.900");
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

export const HNavbar: FC<NavBarProps> = (props) => {
  const [revealed, set_revealed] = useState(true);
  const Wrapped = with_scroll_cbs(
    Inner,
    () => set_revealed(true),
    () => set_revealed(false)
  );

  return <Wrapped revealed={revealed} {...props} />;
};
