import { NextRequest, NextResponse } from "next/server";

export default function middleware(req: NextRequest) {
  console.log(">> middleware.tsx >> req.url", req.url);
  const url = new URL(process.env.API_URL! + req.nextUrl.pathname);
  for (const [key, value] of req.nextUrl.searchParams) {
    url.searchParams.set(key, value);
  }
  console.log("🚀 ~ middleware ~ url:", url.toString());

  return NextResponse.rewrite(url, {
    headers: {
      ...req.headers,
    },
  });
}

export const config = {
  matcher: ["/api/:path*"],
};
