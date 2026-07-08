import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PaperPilot",
  description: "Citation-grounded literature mining for biomedical AI papers",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
