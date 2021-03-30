import "../styles/globals.css";
import { ChakraProvider } from "@chakra-ui/react";
import React from "react";
import { AppProps } from "next/app";
import Head from "next/head";
import Skull from "../images/skull/DTWMSkull-16.png";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <ChakraProvider>
      <Head>
        {/* favicon stuff */}
        <link
          rel="apple-touch-icon"
          sizes="180x180"
          href="/apple-touch-icon.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="32x32"
          href="/favicon-32x32.png"
        />
        <link
          rel="icon"
          type="image/png"
          sizes="16x16"
          href="/favicon-16x16.png"
        />
        <link rel="manifest" href="/site.webmanifest" />
        <link rel="mask-icon" href="/safari-pinned-tab.svg" color="#5bbad5" />
        <meta name="msapplication-TileColor" content="#9f00a7" />
        <meta name="theme-color" content="#e60ded" />

        {/* OpenGraph stuff */}
        <meta property="og:site_name" content="DTWM" />
        <meta property="og:url" content="https://joindtwm.vercel.app/" />
        <meta property="og:description" content="" />
        <meta property="og:type" content="website" />
        <meta property="og:image" content="images/skull/DTWMSkull.big.png" />
      </Head>
      <Component {...pageProps} />
    </ChakraProvider>
  );
}

export default MyApp;
