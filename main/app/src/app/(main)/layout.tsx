import { AppMetaData, NavLinks } from "@/app/global/data";
import AppFooter from "@/components/shared/app-footer";
import { AppSidebar } from "@/components/shared/app-sidebar";
import AppTopbar from "@/components/shared/app-topbar";
import { SidebarProvider } from "@/components/ui/sidebar";
import { Toaster } from "sonner";
import SessionWrapper from "../../../wrappers/SessionWrapper";
import InitCartWrapper from "../../../wrappers/InitCartWrapper";

export default function MainLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <SessionWrapper>
      <InitCartWrapper>
        <SidebarProvider>
          <div className="block md:hidden">
            <AppSidebar LogoIcon={AppMetaData.icon} logoText={AppMetaData.title} />
          </div>
          <main className=" w-full">
            <AppTopbar navlinks={NavLinks} LogoIcon={AppMetaData.icon} logoText={AppMetaData.title} />
            {children}
            <Toaster />
          </main>
        </SidebarProvider>
        <AppFooter navlinks={NavLinks} LogoIcon={AppMetaData.icon} logoText={AppMetaData.title} />
      </InitCartWrapper>
    </SessionWrapper>
  );
}
