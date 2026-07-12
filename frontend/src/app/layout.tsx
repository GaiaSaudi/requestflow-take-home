import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "RequestFlow",
  description: "Senior full-stack production change exercise",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
