import { Link } from "react-router-dom";
import { Presentation, ArrowRight, Sparkles, Zap, Shield } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";

export default function Index() {
  const { isAuthenticated } = useAuth();

  return (
    <div className="min-h-screen">
      {/* Background decoration */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-60 -top-60 h-[500px] w-[500px] rounded-full bg-primary/10 blur-3xl animate-pulse-glow" />
        <div className="absolute -bottom-60 -right-60 h-[500px] w-[500px] rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute left-1/2 top-1/3 h-60 w-60 -translate-x-1/2 rounded-full bg-primary/10 blur-3xl" />
      </div>

      {/* Header */}
      <header className="relative z-10 p-6">
        <nav className="mx-auto flex max-w-6xl items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 glow">
              <Presentation className="h-5 w-5 text-primary" />
            </div>
            <span className="font-display text-xl font-bold text-foreground">
              Slide<span className="gradient-text">AI</span>
            </span>
          </div>
          <div className="flex items-center gap-3">
            {isAuthenticated ? (
              <Button asChild variant="glow">
                <Link to="/dashboard">Dashboard</Link>
              </Button>
            ) : (
              <>
                <Button asChild variant="ghost">
                  <Link to="/login">Sign in</Link>
                </Button>
                <Button asChild variant="glow">
                  <Link to="/signup">Get Started</Link>
                </Button>
              </>
            )}
          </div>
        </nav>
      </header>

      {/* Hero */}
      <main className="relative z-10 px-6 py-20 md:py-32">
        <div className="mx-auto max-w-4xl text-center animate-slide-up">
          <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-2 text-sm text-primary">
            <Sparkles className="h-4 w-4" />
            AI-Powered Presentation Generator
          </div>
          <h1 className="font-display text-5xl font-bold leading-tight text-foreground md:text-7xl">
            Create presentations
            <span className="gradient-text block">like magic</span>
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-muted-foreground md:text-xl">
            Generate professional PowerPoint presentations in seconds. Just enter your topic, 
            and let our AI do the rest.
          </p>
          <div className="mt-10 flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
            <Button asChild variant="glow" size="xl">
              <Link to={isAuthenticated ? "/dashboard" : "/signup"}>
                Start Creating Free
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button asChild variant="glass" size="xl">
              <Link to="/login">Sign in</Link>
            </Button>
          </div>
        </div>

        {/* Features Grid */}
        <div className="mx-auto mt-32 max-w-5xl">
          <h2 className="mb-12 text-center font-display text-3xl font-bold text-foreground">
            Why choose SlideAI?
          </h2>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                icon: Sparkles,
                title: "AI-Powered Content",
                description:
                  "Our advanced AI understands your topic and generates relevant, engaging content for each slide.",
              },
              {
                icon: Zap,
                title: "Lightning Fast",
                description:
                  "Get a complete presentation in seconds, not hours. Focus on what matters most.",
              },
              {
                icon: Shield,
                title: "Professional Quality",
                description:
                  "Every presentation is designed to look professional and polished, ready for any audience.",
              },
            ].map((feature, index) => (
              <div
                key={feature.title}
                className="glass group rounded-2xl p-8 transition-all duration-300 hover:border-primary/30 hover:glow"
                style={{ animationDelay: `${index * 100}ms` }}
              >
                <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-primary/10 transition-all duration-300 group-hover:bg-primary/20">
                  <feature.icon className="h-7 w-7 text-primary" />
                </div>
                <h3 className="font-display text-xl font-semibold text-foreground">
                  {feature.title}
                </h3>
                <p className="mt-3 text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* CTA Section */}
        <div className="mx-auto mt-32 max-w-3xl text-center">
          <div className="glass rounded-3xl p-12">
            <h2 className="font-display text-3xl font-bold text-foreground md:text-4xl">
              Ready to create your first presentation?
            </h2>
            <p className="mx-auto mt-4 max-w-lg text-muted-foreground">
              Join thousands of users who are already creating stunning presentations with AI.
            </p>
            <Button asChild variant="glow" size="xl" className="mt-8">
              <Link to={isAuthenticated ? "/dashboard" : "/signup"}>
                Get Started Now
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="relative z-10 border-t border-border p-6 text-center text-sm text-muted-foreground">
        <p>© 2024 SlideAI. Powered by AI.</p>
      </footer>
    </div>
  );
}
