import { ReactNode } from "react";
import { Presentation } from "lucide-react";

interface AuthLayoutProps {
  children: ReactNode;
  title: string;
  subtitle: string;
}

export function AuthLayout({ children, title, subtitle }: AuthLayoutProps) {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      {/* Background decoration */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-40 -top-40 h-80 w-80 rounded-full bg-primary/10 blur-3xl" />
        <div className="absolute -bottom-40 -right-40 h-80 w-80 rounded-full bg-primary/5 blur-3xl" />
      </div>

      <div className="relative w-full max-w-md animate-slide-up">
        {/* Logo */}
        <div className="mb-8 flex items-center justify-center gap-3">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 glow">
            <Presentation className="h-6 w-6 text-primary" />
          </div>
          <span className="font-display text-2xl font-bold text-foreground">
            Slide<span className="gradient-text">AI</span>
          </span>
        </div>

        {/* Card */}
        <div className="glass rounded-2xl p-8 shadow-2xl">
          <div className="mb-6 text-center">
            <h1 className="font-display text-2xl font-bold text-foreground">{title}</h1>
            <p className="mt-2 text-sm text-muted-foreground">{subtitle}</p>
          </div>
          {children}
        </div>
      </div>
    </div>
  );
}
