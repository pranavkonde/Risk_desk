import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Pacifica Risk Desk",
  description: "Modern Pacifica perps analytics terminal with funding, execution, and risk intelligence.",
  metadataBase: new URL("https://pacifica-riskdesk.vercel.app"),
  openGraph: {
    title: "Pacifica Risk Desk",
    description: "Funding radar, execution analytics, and risk monitoring for Pacifica traders.",
    type: "website",
    images: [{ url: "/opengraph-image", width: 1200, height: 630 }],
  },
  twitter: {
    card: "summary_large_image",
    title: "Pacifica Risk Desk",
    description: "Funding radar, execution analytics, and risk monitoring for Pacifica traders.",
    images: ["/opengraph-image"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.variable}>{children}</body>
    </html>
  );
}
