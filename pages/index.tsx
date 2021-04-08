import React from "react";
import Head from "next/head";
import Image from "next/image";
import ThemeTest from "../components/theme_test";
import Article from "../components/templates/article";
import { Center, Heading } from "@chakra-ui/react";

const Home = () => (
  <>
    <Head>
      <title>DTWM - Home</title>
    </Head>
    <Article>
      <Center>
        <Image width={200} height={200} src="/images/skull/DTWMSkull.big.png" />
      </Center>
      <Heading fontSize="2xl">Welcome to the DTWM website :^)</Heading>
      <ThemeTest />
    </Article>
  </>
);

const title = "DTWM - Home";

export default Home;
