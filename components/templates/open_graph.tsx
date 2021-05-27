import React, { FC } from "react";
import Head from "next/head";

export interface OGProps {
  site_name?: string;
  url?: string;
  description?: string;
  type?: string;
  image_url?: string;
}

const OG: FC<OGProps> = ({
  site_name = "DTWM",
  url = "https://joindtwm.vercel.app/",
  description = "The DTWM weebs are invading your computer...",
  type = "website",
  image_url = "https://joindtwm.vercel.app/_next/image?url=%2Fimages%2Fskull%2FDTWMSkull.big.png&w=256&q=75",
}) => {
  return (
    <Head>
      {/* OpenGraph stuff */}
      <meta property="og:site_name" content={site_name} key="ogsitename" />
      <meta property="og:url" content={url} key="ogurl" />
      <meta property="og:description" content={description} key="ogdesc" />
      <meta property="og:type" content={type} key="ogtype" />
      <meta property="og:image" content={image_url} key="ogimage" />
    </Head>
  );
};

export default OG;
