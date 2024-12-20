import React from "react";

function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="w-svh h-svh flex items-center justify-center ">
      {children}
    </div>
  );
}

export default AuthLayout;
