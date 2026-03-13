'use client';

import { useState, useEffect } from 'react';
import { Plus, FileText, Pencil, Trash2, ExternalLink } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import CreateProposalModal from '@/components/CreateProposalModal';
import Link from 'next/link';

export default function Dashboard() {
  const [proposals, setProposals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingProposal, setEditingProposal] = useState(null);

  useEffect(() => {
    fetchProposals();
  }, []);

  const fetchProposals = async () => {
    try {
      const response = await fetch('/api/proposals');
      const data = await response.json();
      setProposals(data.proposals || []);
    } catch (error) {
      console.error('Error fetching proposals:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Tem certeza que deseja excluir esta proposta?')) return;

    try {
      await fetch(`/api/proposals/${id}`, { method: 'DELETE' });
      fetchProposals();
    } catch (error) {
      console.error('Error deleting proposal:', error);
    }
  };

  const handleEdit = (proposal) => {
    setEditingProposal(proposal);
    setShowCreateModal(true);
  };

  const handleModalClose = () => {
    setShowCreateModal(false);
    setEditingProposal(null);
    fetchProposals();
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-zinc-950 to-black">
      {/* Header */}
      <div className="border-b border-zinc-800 bg-black/50 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-white">
                Gerador de <span className="text-lime-400">Propostas</span>
              </h1>
              <p className="text-zinc-400 mt-1">Crie e gerencie propostas comerciais profissionais</p>
            </div>
            <Button
              onClick={() => setShowCreateModal(true)}
              className="bg-lime-400 hover:bg-lime-500 text-black font-semibold"
              size="lg"
            >
              <Plus className="w-5 h-5 mr-2" />
              Nova Proposta
            </Button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-lime-400"></div>
          </div>
        ) : proposals.length === 0 ? (
          <Card className="bg-zinc-900/50 border-zinc-800 text-center py-16">
            <CardContent>
              <FileText className="w-16 h-16 mx-auto text-zinc-600 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Nenhuma proposta criada</h3>
              <p className="text-zinc-400 mb-6">Comece criando sua primeira proposta comercial</p>
              <Button
                onClick={() => setShowCreateModal(true)}
                className="bg-lime-400 hover:bg-lime-500 text-black font-semibold"
              >
                <Plus className="w-5 h-5 mr-2" />
                Criar Primeira Proposta
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {proposals.map((proposal) => (
              <Card
                key={proposal.id}
                className="bg-zinc-900/50 border-zinc-800 hover:border-lime-400/50 transition-all duration-300 group"
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      {proposal.clientLogo && (
                        <img
                          src={proposal.clientLogo}
                          alt={proposal.companyName}
                          className="w-12 h-12 object-contain mb-3 rounded"
                        />
                      )}
                      <CardTitle className="text-white text-lg mb-1">
                        {proposal.companyName}
                      </CardTitle>
                      <CardDescription className="text-zinc-400">
                        {proposal.clientName}
                      </CardDescription>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-zinc-300 mb-4 line-clamp-2">
                    {proposal.title}
                  </p>
                  <div className="flex gap-2">
                    <Link href={`/proposal/${proposal.id}`} className="flex-1">
                      <Button
                        variant="outline"
                        className="w-full border-lime-400/50 text-lime-400 hover:bg-lime-400/10"
                        size="sm"
                      >
                        <ExternalLink className="w-4 h-4 mr-2" />
                        Ver
                      </Button>
                    </Link>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(proposal)}
                      className="border-zinc-700 text-zinc-300 hover:bg-zinc-800"
                    >
                      <Pencil className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(proposal.id)}
                      className="border-red-900/50 text-red-400 hover:bg-red-950/50"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>

      {/* Create/Edit Modal */}
      {showCreateModal && (
        <CreateProposalModal
          isOpen={showCreateModal}
          onClose={handleModalClose}
          proposal={editingProposal}
        />
      )}
    </div>
  );
}