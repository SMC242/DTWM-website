import "../styles/globals.css";
import React, { FC } from "react";
import type { AppProps } from "next/app";
import Head from "next/head";
import { CustomChakraProvider } from "../theme";
import { HNavbar } from "../components/navigation/navbar";
import Header from "../components/templates/header";

const MyApp: FC<AppProps> = ({ Component, pageProps }) => {
  const links = [
    {
      text: "Home",
      route: "/",
    },
    {
      text: "Info",
      route: "/info",
    },
    {
      text: "Discord",
      route: "https://joindtwm.vercel.app/join",
    },
    {
      text: "Training Docs",
      route: "/training/training-home",
    },
    { text: "Outfit Trees", route: "/outfit_trees/outfit_trees_home" },
  ];

  return (
    <CustomChakraProvider>
      <Header />
      <HNavbar links={links} />
      <Component {...pageProps} />
    </CustomChakraProvider>
  );
};

export default MyApp;
