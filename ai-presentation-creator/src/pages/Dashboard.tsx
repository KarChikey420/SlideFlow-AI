import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Presentation,
  Download,
  Loader2,
  LogOut,
  Sparkles,
  Layers,
  Minus,
  Plus,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/contexts/AuthContext";
import { generatePPT } from "@/lib/api";
import { useToast } from "@/hooks/use-toast";

export default function Dashboard() {
  const [topic, setTopic] = useState("");
  const [slideCount, setSlideCount] = useState(10);
  const [isGenerating, setIsGenerating] = useState(false);
  const { token, logout } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();

  const handleLogout = () => {
    logout();
    navigate("/login");
    toast({
      title: "Logged out",
      description: "See you next time!",
    });
  };

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token || !topic.trim()) return;

    setIsGenerating(true);

    try {
      const blob = await generatePPT(topic, slideCount, token);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${topic.replace(/\s+/g, "_")}.pptx`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);

      toast({
        title: "Presentation ready!",
        description: "Your PowerPoint has been downloaded.",
      });
    } catch (error) {
      toast({
        title: "Generation failed",
        description: error instanceof Error ? error.message : "Could not generate presentation",
        variant: "destructive",
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const adjustSlideCount = (delta: number) => {
    setSlideCount((prev) => Math.max(3, Math.min(30, prev + delta)));
  };

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Background decoration */}
      <div className="pointer-events-none fixed inset-0 overflow-hidden">
        <div className="absolute -left-40 top-20 h-96 w-96 rounded-full bg-primary/5 blur-3xl" />
        <div className="absolute -right-40 bottom-20 h-96 w-96 rounded-full bg-primary/10 blur-3xl" />
      </div>

      <div className="relative mx-auto max-w-4xl">
        {/* Header */}
        <header className="mb-12 flex items-center justify-between animate-fade-in">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
              <Presentation className="h-5 w-5 text-primary" />
            </div>
            <span className="font-display text-xl font-bold text-foreground">
              Slide<span className="gradient-text">AI</span>
            </span>
          </div>
          <Button variant="ghost" size="sm" onClick={handleLogout}>
            <LogOut className="mr-2 h-4 w-4" />
            Logout
          </Button>
        </header>

        {/* Main Content */}
        <main className="animate-slide-up">
          <div className="mb-10 text-center">
            <h1 className="font-display text-4xl font-bold text-foreground md:text-5xl">
              Create stunning presentations
              <span className="gradient-text block mt-1">in seconds</span>
            </h1>
            <p className="mx-auto mt-4 max-w-lg text-muted-foreground">
              Enter any topic and let AI generate a professional PowerPoint presentation for you.
            </p>
          </div>

          {/* Generator Card */}
          <div className="glass mx-auto max-w-2xl rounded-2xl p-8 shadow-2xl">
            <form onSubmit={handleGenerate} className="space-y-6">
              {/* Topic Input */}
              <div className="space-y-3">
                <label className="flex items-center gap-2 text-sm font-medium text-foreground">
                  <Sparkles className="h-4 w-4 text-primary" />
                  Presentation Topic
                </label>
                <Input
                  type="text"
                  placeholder="e.g., Introduction to Machine Learning"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  className="h-14 text-base"
                  required
                />
              </div>

              {/* Slide Count */}
              <div className="space-y-3">
                <label className="flex items-center gap-2 text-sm font-medium text-foreground">
                  <Layers className="h-4 w-4 text-primary" />
                  Number of Slides
                </label>
                <div className="flex items-center gap-4">
                  <Button
                    type="button"
                    variant="outline"
                    size="icon"
                    onClick={() => adjustSlideCount(-1)}
                    disabled={slideCount <= 3}
                  >
                    <Minus className="h-4 w-4" />
                  </Button>
                  <div className="flex-1">
                    <div className="relative">
                      <input
                        type="range"
                        min="3"
                        max="30"
                        value={slideCount}
                        onChange={(e) => setSlideCount(Number(e.target.value))}
                        className="w-full h-2 rounded-full appearance-none cursor-pointer bg-secondary [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-5 [&::-webkit-slider-thumb]:w-5 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary [&::-webkit-slider-thumb]:shadow-lg [&::-webkit-slider-thumb]:glow [&::-webkit-slider-thumb]:cursor-pointer"
                      />
                    </div>
                    <div className="mt-2 flex justify-between text-xs text-muted-foreground">
                      <span>3</span>
                      <span className="text-sm font-semibold text-primary">{slideCount} slides</span>
                      <span>30</span>
                    </div>
                  </div>
                  <Button
                    type="button"
                    variant="outline"
                    size="icon"
                    onClick={() => adjustSlideCount(1)}
                    disabled={slideCount >= 30}
                  >
                    <Plus className="h-4 w-4" />
                  </Button>
                </div>
              </div>

              {/* Generate Button */}
              <Button
                type="submit"
                variant="glow"
                size="xl"
                className="w-full"
                disabled={isGenerating || !topic.trim()}
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="h-5 w-5 animate-spin" />
                    Generating presentation...
                  </>
                ) : (
                  <>
                    <Download className="h-5 w-5" />
                    Generate & Download
                  </>
                )}
              </Button>
            </form>
          </div>

          {/* Features */}
          <div className="mt-12 grid gap-6 md:grid-cols-3">
            {[
              {
                icon: Sparkles,
                title: "AI-Powered",
                description: "Advanced AI generates relevant content for your topic",
              },
              {
                icon: Layers,
                title: "Customizable",
                description: "Choose the number of slides you need",
              },
              {
                icon: Download,
                title: "Instant Download",
                description: "Get your PPTX file ready in seconds",
              },
            ].map((feature) => (
              <div
                key={feature.title}
                className="glass rounded-xl p-6 text-center transition-all duration-300 hover:border-primary/30"
              >
                <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="font-display font-semibold text-foreground">{feature.title}</h3>
                <p className="mt-2 text-sm text-muted-foreground">{feature.description}</p>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
