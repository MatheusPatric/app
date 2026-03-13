'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { CheckCircle2, MessageCircle, ArrowLeft, Copy, ExternalLink, Sparkles } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import confetti from 'canvas-confetti';

export default function ObrigadoPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [proposal, setProposal] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [countdown, setCountdown] = useState(5);
  const selectedPlan = searchParams.get('plan');

  useEffect(() => {
    if (params?.id) {
      fetchProposal();
      // Trigger confetti animation
      const duration = 3000;
      const animationEnd = Date.now() + duration;
      const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 0 };

      function randomInRange(min, max) {
        return Math.random() * (max - min) + min;
      }

      const interval = setInterval(function() {
        const timeLeft = animationEnd - Date.now();

        if (timeLeft <= 0) {
          return clearInterval(interval);
        }

        const particleCount = 50 * (timeLeft / duration);
        
        confetti(Object.assign({}, defaults, {
          particleCount,
          origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 }
        }));
        confetti(Object.assign({}, defaults, {
          particleCount,
          origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 }
        }));
      }, 250);
    }
  }, [params?.id]);

  // Countdown timer
  useEffect(() => {
    if (proposal && countdown > 0) {
      const timer = setTimeout(() => {
        setCountdown(countdown - 1);
      }, 1000);
      return () => clearTimeout(timer);
    } else if (countdown === 0) {
      handleWhatsApp();
    }
  }, [countdown, proposal]);

  const fetchProposal = async () => {
    try {
      const response = await fetch(`/api/proposals/${params.id}`);
      const data = await response.json();
      setProposal(data.proposal);
    } catch (error) {
      console.error('Error fetching proposal:', error);
    } finally {
      setLoading(false);
    }
  };

  const getProposalUrl = () => {
    if (typeof window !== 'undefined') {
      return `${window.location.origin}/proposal/${params.id}`;
    }
    return '';
  };

  const handleCopyLink = () => {
    const url = getProposalUrl();
    navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleWhatsApp = () => {
    if (!proposal) return;
    
    const proposalUrl = getProposalUrl();
    const planText = selectedPlan ? `\n\nPlano escolhido: ${selectedPlan}` : '';
    const message = `Olá! 🎉

Acabei de aceitar a proposta de gestão de conteúdo!${planText}

Estou muito animado(a) para começar essa parceria com a ${proposal.brandName || 'Zeri Solutions'}!

Proposta aceita: ${proposalUrl}

Podemos conversar sobre os próximos passos?`;

    const phone = proposal.contactWhatsApp?.replace(/\D/g, '') || '';
    const whatsappUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  const handleSkipCountdown = () => {
    setCountdown(0);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-lime-400"></div>
      </div>
    );
  }

  if (!proposal) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-white mb-2">Proposta não encontrada</h1>
          <Button onClick={() => router.push('/')} className="mt-4">
            Voltar ao Início
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-zinc-950 to-black flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        {/* Success Animation */}
        <div className="text-center mb-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
          <div className="inline-flex items-center justify-center w-24 h-24 bg-lime-400 rounded-full mb-6 animate-bounce">
            <CheckCircle2 className="w-12 h-12 text-black" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold text-white mb-4">
            Parabéns! 🎉
          </h1>
          <p className="text-xl text-lime-400 font-semibold mb-2">
            Proposta Aceita com Sucesso!
          </p>
        </div>

        {/* Main Card */}
        <Card className="bg-zinc-900/80 backdrop-blur-sm border-zinc-800 p-8 animate-in fade-in slide-in-from-bottom-8 duration-700 delay-200">
          <div className="text-center mb-8">
            <Sparkles className="w-8 h-8 text-lime-400 mx-auto mb-4" />
            <h2 className="text-2xl font-bold text-white mb-4">
              Obrigado pela Confiança!
            </h2>
            {selectedPlan && (
              <div className="mb-4 inline-flex items-center gap-2 bg-lime-400/20 border-2 border-lime-400 rounded-lg px-6 py-3">
                <CheckCircle2 className="w-5 h-5 text-lime-400" />
                <span className="text-white font-bold">Plano: {selectedPlan}</span>
              </div>
            )}
            <p className="text-zinc-300 text-lg leading-relaxed">
              Estamos muito felizes em tê-lo(a) como cliente da <span className="text-lime-400 font-semibold">{proposal.brandName || 'Zeri Solutions'}</span>!
            </p>
            <p className="text-zinc-400 mt-4">
              Sua jornada de crescimento digital começa agora. 🚀
            </p>
          </div>

          {/* Proposal Link */}
          <div className="bg-zinc-800/50 rounded-lg p-4 mb-6">
            <p className="text-zinc-400 text-sm mb-2">Link da sua proposta:</p>
            <div className="flex items-center gap-2">
              <input
                type="text"
                value={getProposalUrl()}
                readOnly
                className="flex-1 bg-zinc-900 border border-zinc-700 rounded px-3 py-2 text-sm text-white"
              />
              <Button
                onClick={handleCopyLink}
                size="sm"
                variant="outline"
                className="border-lime-400/50 text-lime-400 hover:bg-lime-400/10"
              >
                {copied ? (
                  <CheckCircle2 className="w-4 h-4" />
                ) : (
                  <Copy className="w-4 h-4" />
                )}
              </Button>
            </div>
          </div>

          {/* Countdown */}
          {countdown > 0 && (
            <div className="text-center mb-6 py-4 bg-lime-400/10 rounded-lg border border-lime-400/30">
              <p className="text-zinc-300 mb-2">
                Abrindo WhatsApp em <span className="text-lime-400 font-bold text-2xl">{countdown}</span> segundos...
              </p>
              <Button
                onClick={handleSkipCountdown}
                variant="link"
                className="text-lime-400 hover:text-lime-300 text-sm"
              >
                Pular contagem
              </Button>
            </div>
          )}

          {/* Action Buttons */}
          <div className="space-y-3">
            <Button
              onClick={handleWhatsApp}
              className="w-full bg-lime-400 hover:bg-lime-500 text-black font-bold text-lg py-6"
              size="lg"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              Continuar no WhatsApp
            </Button>

            <div className="flex gap-3">
              <Button
                onClick={() => router.push(`/proposal/${params.id}`)}
                variant="outline"
                className="flex-1 border-zinc-700 text-zinc-300 hover:bg-zinc-800"
              >
                <ArrowLeft className="w-4 h-4 mr-2" />
                Ver Proposta
              </Button>
              <Button
                onClick={handleCopyLink}
                variant="outline"
                className="flex-1 border-zinc-700 text-zinc-300 hover:bg-zinc-800"
              >
                <Copy className="w-4 h-4 mr-2" />
                {copied ? 'Copiado!' : 'Copiar Link'}
              </Button>
            </div>
          </div>

          {/* Next Steps */}
          <div className="mt-8 pt-6 border-t border-zinc-800">
            <h3 className="text-white font-semibold mb-4 flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-lime-400" />
              Próximos Passos:
            </h3>
            <ul className="space-y-3 text-zinc-300">
              <li className="flex items-start gap-3">
                <span className="text-lime-400 font-bold">1.</span>
                <span>Converse conosco no WhatsApp para alinhar detalhes</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-lime-400 font-bold">2.</span>
                <span>Agendaremos uma reunião estratégica inicial</span>
              </li>
              <li className="flex items-start gap-3">
                <span className="text-lime-400 font-bold">3.</span>
                <span>Começaremos o planejamento do seu conteúdo</span>
              </li>
            </ul>
          </div>
        </Card>

        {/* Footer Message */}
        <div className="text-center mt-6 animate-in fade-in duration-700 delay-500">
          <p className="text-zinc-400 text-sm">
            Estamos ansiosos para começar essa jornada com você! ✨
          </p>
        </div>
      </div>
    </div>
  );
}
