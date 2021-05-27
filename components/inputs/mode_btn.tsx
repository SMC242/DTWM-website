import React from "react";
import { IconButton, useColorMode } from "@chakra-ui/react";
import { WiDaySunny } from "react-icons/wi";
import { IoIosCloudyNight } from "react-icons/io";

const ModeButton = ({ ...button_props }) => {
  const { colorMode, toggleColorMode } = useColorMode();
  const icon = colorMode === "light" ? <WiDaySunny /> : <IoIosCloudyNight />;

  return (
    <IconButton
      aria-label="Change colour mode"
      icon={icon}
      onClick={toggleColorMode}
      maxWidth="3rem"
      {...button_props}
    />
  );
};

export default ModeButton;
