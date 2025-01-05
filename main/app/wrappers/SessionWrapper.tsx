"use client";
import { useSessionQuery } from "@/store/api/auth";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function SessionWrapper({ children }: { children: React.ReactNode }) {
  const { data, error } = useSessionQuery();
  const router = useRouter();
  useEffect(() => {
    if (error) {
      router.push("/login");
    }
  }, [data]);

  return <>{children}</>;
}
