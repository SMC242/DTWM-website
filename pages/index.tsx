import React from "react";
import Head from "next/head";
import Image from "next/image";
import ThemeTest from "../components/theme_test";

const Home = () => (
  <>
    <Head>
      <title>DTWM - Home</title>
    </Head>
    <h3>Welcome to the DTWM website :^)</h3>
    <Image width={200} height={200} src="/images/skull/DTWMSkull.big.png" />
    <ThemeTest />
  </>
);

const title = "DTWM - Home";

export default Home;
