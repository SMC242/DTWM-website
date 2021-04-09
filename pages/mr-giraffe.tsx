import React, { PropsWithChildren, FC } from "react";
import Image from "next/image";
import Article from "../components/templates/article";
import { motion } from "framer-motion";
import { Box, Heading, Text } from "@chakra-ui/react";

const MrGeraffe = () => (
  <Image src="/images/MrGeRaffe.png" width={150} height="auto" />
);
type Wrapper = FC<PropsWithChildren<{}>>;
const MotionBox = motion(Box);
const Spinning: Wrapper = ({ children }) => (
  <MotionBox
    animate={{ rotate: 360 }}
    transition={{ duration: 1.5, repeat: Infinity }}
  >
    {children}
  </MotionBox>
);

const SpinningGiraffe = () => (
  <Spinning>
    <MrGeraffe />
  </Spinning>
);

const Tennis: Wrapper = ({ children }) => (
  <MotionBox
    animate={{ x: 350 }}
    transition={{ duration: 2, repeatType: "reverse", repeat: Infinity }}
  >
    {children}
  </MotionBox>
);

const BouncingGiraffe = () => (
  <Tennis>
    <SpinningGiraffe />
  </Tennis>
);

const GiraffePage = () => (
  <Article>
    <Heading>This is Mr Ge Rafe's hideout</Heading>
    <Text>
      Congratulations for finding such a hidden place. Your reward is below...
    </Text>
    <SpinningGiraffe />
    <BouncingGiraffe />
  </Article>
);

export default GiraffePage;
