"use client";
import ServiceWorkerProvider from "@/providers/service-worker";
import { store } from "@/store/store";
import React from "react";
import { Provider } from "react-redux";

function RootProviders({ children }: { children: React.ReactNode }) {
  return (
    <ServiceWorkerProvider>
      <Provider store={store}>{children}</Provider>;
    </ServiceWorkerProvider>
  );
}

export default RootProviders;
