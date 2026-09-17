import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "hunter/seeker",
  description: "An agentic job board that matches Seekers to jobs, not the other way round.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="flex min-h-full flex-col">{children}</body>
    </html>
  );
}
