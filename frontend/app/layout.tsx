import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI SQL Query Assistant",
  description: "Convert natural language to SQL queries with AI",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="h-full">
      <body className="h-full bg-zinc-50 dark:bg-zinc-950 antialiased">
        {children}
      </body>
    </html>
  );
}