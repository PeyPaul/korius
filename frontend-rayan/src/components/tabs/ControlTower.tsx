import React from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { AlertTriangle, Clock, Package, Phone, PhoneCall, CheckCircle2, AlertCircle, DollarSign } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from "@/components/ui/dialog";

const ControlTower = () => {
  const { toast } = useToast();
  const [transcriptDialog, setTranscriptDialog] = React.useState<{ open: boolean; content: string }>({
    open: false,
    content: "",
  });

  const handleUnriskDeliveries = () => {
    toast({
      title: "Unrisking Deliveries",
      description: "AI agents are calling suppliers to follow up on late/uncertain ETAs...",
    });
  };

  const handleRelanceSuppliers = () => {
    toast({
      title: "Relancing Suppliers",
      description: "AI agents are following up with unresponsive suppliers...",
    });
  };

  const handleUpdatePrices = () => {
    toast({
      title: "Price Update Started",
      description: "AI agents are verifying current prices with suppliers...",
    });
  };

  const handleFindNewProducts = () => {
    toast({
      title: "Market Search Initiated",
      description: "AI agents are searching for new products matching your needs...",
    });
  };

  const handleApplyUpdate = (supplier: string) => {
    toast({
      title: "Update Applied",
      description: `Information from ${supplier} has been updated in the system`,
    });
  };

  const handleViewTranscript = (supplier: string, content: string) => {
    setTranscriptDialog({ open: true, content });
  };

  const handleEscalate = (supplier: string) => {
    toast({
      title: "Escalation Created",
      description: `Priority escalation initiated for ${supplier}`,
      variant: "destructive",
    });
  };

  const handleRecall = (supplier: string) => {
    toast({
      title: "Re-calling Supplier",
      description: `Agent is calling ${supplier} again...`,
    });
  };

  return (
    <div className="space-y-6">
      {/* Core Services Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-6 border-l-4 border-l-critical hover:shadow-lg transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-critical/10 rounded-lg">
                <AlertTriangle className="h-5 w-5 text-critical" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Delivery Risks Resolved</p>
                <p className="text-3xl font-bold text-foreground mt-1">3</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Saved <strong>28 min</strong> of ETA checks today
                </p>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-6 border-l-4 border-l-moderate hover:shadow-lg transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-moderate/10 rounded-lg">
                <Phone className="h-5 w-5 text-moderate" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Supplier Follow-ups Sent</p>
                <p className="text-3xl font-bold text-foreground mt-1">7</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Avoided <strong>45 min</strong> of calls & emails
                </p>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-6 border-l-4 border-l-low hover:shadow-lg transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-low/10 rounded-lg">
                <DollarSign className="h-5 w-5 text-low" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Price Checks Completed</p>
                <p className="text-3xl font-bold text-foreground mt-1">12</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Saved <strong>22 min</strong> on manual lookup
                </p>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-6 border-l-4 border-l-primary hover:shadow-lg transition-shadow cursor-pointer">
          <div className="flex items-start justify-between">
            <div className="flex items-start gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Package className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-sm text-muted-foreground">New Product Matches</p>
                <p className="text-3xl font-bold text-foreground mt-1">5</p>
                <p className="text-xs text-muted-foreground mt-1">
                  Replaced <strong>30 min</strong> of market scanning
                </p>
              </div>
            </div>
          </div>
        </Card>
      </div>

      {/* Daily Agents Recap */}
      <Card className="p-6">
        <h2 className="text-lg font-semibold text-foreground mb-4">AI Agent Activity</h2>
        <div className="space-y-3">
          {/* Active Call - Unrisking Delivery */}
          <div className="border border-border rounded-lg p-4 bg-card hover:bg-accent/5 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <div className="h-3 w-3 bg-low rounded-full animate-pulse"></div>
                  <div className="absolute top-0 left-0 h-3 w-3 bg-low rounded-full animate-ping"></div>
                </div>
                <div>
                  <p className="font-medium text-foreground">Unrisking Late Delivery</p>
                  <p className="text-sm text-muted-foreground">Medisupply SAS - Following up on Ibuprofen 400mg ETA</p>
                </div>
              </div>
              <Badge variant="outline" className="bg-low/10 text-low border-low/20">
                In Progress
              </Badge>
            </div>
            <div className="flex items-center gap-2 text-xs text-muted-foreground">
              <Clock className="h-3 w-3" />
              <span>Started 2 min ago</span>
            </div>
          </div>

          {/* Completed Call - Price Update */}
          <div className="border border-border rounded-lg p-4 bg-card hover:bg-accent/5 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <div>
                  <p className="font-medium text-foreground">Price Update Complete</p>
                  <p className="text-sm text-muted-foreground">PharmaCore Europe - Updated pricing for 8 products</p>
                </div>
              </div>
              <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">
                Completed
              </Badge>
            </div>
            <div className="flex items-center gap-2 mt-3">
              <Button size="sm" variant="outline" onClick={() => handleApplyUpdate("PharmaCore Europe")}>
                Apply Update
              </Button>
              <Button
                size="sm"
                variant="ghost"
                onClick={() =>
                  handleViewTranscript(
                    "PharmaCore Europe",
                    "Call transcript showing price updates for 8 products including Paracetamol 500mg (new price: €4.20), Ibuprofen 400mg (new price: €6.80)...",
                  )
                }
              >
                View Transcript
              </Button>
            </div>
          </div>

          {/* Failed Call - Relance Needed */}
          <div className="border border-border rounded-lg p-4 bg-card hover:bg-accent/5 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <AlertCircle className="h-5 w-5 text-critical" />
                <div>
                  <p className="font-medium text-foreground">Supplier Not Responding</p>
                  <p className="text-sm text-muted-foreground">BioMed Labs - No response on Amoxicillin availability</p>
                </div>
              </div>
              <Badge variant="outline" className="bg-critical/10 text-critical border-critical/20">
                Action Required
              </Badge>
            </div>
            <div className="flex items-center gap-2 mt-3">
              <Button size="sm" variant="destructive" onClick={() => handleEscalate("BioMed Labs")}>
                Escalate
              </Button>
              <Button size="sm" variant="outline" onClick={() => handleRecall("BioMed Labs")}>
                Re-call
              </Button>
            </div>
          </div>

          {/* Completed - New Product Found */}
          <div className="border border-border rounded-lg p-4 bg-card hover:bg-accent/5 transition-colors">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-3">
                <CheckCircle2 className="h-5 w-5 text-green-500" />
                <div>
                  <p className="font-medium text-foreground">New Product Match Found</p>
                  <p className="text-sm text-muted-foreground">
                    Alternative supplier for Flu Relief - 15% cost savings identified
                  </p>
                </div>
              </div>
              <Badge variant="outline" className="bg-green-500/10 text-green-500 border-green-500/20">
                Completed
              </Badge>
            </div>
            <div className="flex items-center gap-2 mt-3">
              <Button
                size="sm"
                variant="outline"
                onClick={() =>
                  handleViewTranscript(
                    "Market Research",
                    "Found: Generic Flu Relief Syrup 150ml from HealthPlus Distribution - Price: €8.50 (vs current €10.00), Lead time: 3 days...",
                  )
                }
              >
                View Details
              </Button>
            </div>
          </div>
        </div>
      </Card>

      {/* Transcript Dialog */}
      <Dialog open={transcriptDialog.open} onOpenChange={(open) => setTranscriptDialog({ ...transcriptDialog, open })}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Call Transcript</DialogTitle>
            <DialogDescription>AI agent conversation transcript</DialogDescription>
          </DialogHeader>
          <div className="mt-4 p-4 bg-muted rounded-lg max-h-96 overflow-y-auto">
            <p className="text-sm text-foreground whitespace-pre-wrap">{transcriptDialog.content}</p>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default ControlTower;
