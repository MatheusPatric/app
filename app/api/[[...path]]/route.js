export const config = {
  api: {
    bodyParser: {
      sizeLimit: '10mb',
    },
  },
};

import { MongoClient } from 'mongodb';
import { NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

const uri = process.env.MONGO_URL;
const dbName = process.env.DB_NAME || 'proposal_generator';

let cachedClient = null;
let cachedDb = null;

async function connectToDatabase() {
  if (cachedClient && cachedDb) {
    return { client: cachedClient, db: cachedDb };
  }

  const client = await MongoClient.connect(uri, {
    maxPoolSize: 10,
    serverSelectionTimeoutMS: 5000,
  });

  const db = client.db(dbName);
  cachedClient = client;
  cachedDb = db;

  return { client, db };
}

// Helper to handle CORS
function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };
}

export async function OPTIONS() {
  return NextResponse.json({}, { headers: corsHeaders() });
}

export async function GET(request) {
  try {
    const { db } = await connectToDatabase();
    const { pathname, searchParams } = new URL(request.url);
    const path = pathname.replace('/api/', '');

    // Get all proposals
    if (path === 'proposals') {
      const proposals = await db
        .collection('proposals')
        .find({})
        .sort({ createdAt: -1 })
        .toArray();
      return NextResponse.json({ proposals }, { headers: corsHeaders() });
    }

    // Get single proposal by ID
    if (path.startsWith('proposals/')) {
      const id = path.split('/')[1];
      const proposal = await db.collection('proposals').findOne({ id });
      
      if (!proposal) {
        return NextResponse.json(
          { error: 'Proposal not found' },
          { status: 404, headers: corsHeaders() }
        );
      }
      
      return NextResponse.json({ proposal }, { headers: corsHeaders() });
    }

    return NextResponse.json(
      { error: 'Route not found' },
      { status: 404, headers: corsHeaders() }
    );
  } catch (error) {
    console.error('GET Error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500, headers: corsHeaders() }
    );
  }
}

export async function POST(request) {
  try {
    const { db } = await connectToDatabase();
    const { pathname } = new URL(request.url);
    const path = pathname.replace('/api/', '');
    const body = await request.json();

    // Create new proposal
    if (path === 'proposals') {
      const proposal = {
        id: uuidv4(),
        ...body,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
      };

      await db.collection('proposals').insertOne(proposal);
      return NextResponse.json(
        { proposal },
        { status: 201, headers: corsHeaders() }
      );
    }

    // Upload image
    if (path === 'upload-image') {
      // In this case, body contains base64 image data
      return NextResponse.json(
        { imageUrl: body.imageData },
        { headers: corsHeaders() }
      );
    }

    // AI Generate text
    if (path === 'ai-generate') {
      const { prompt, fieldType } = body;
      
      // Simple AI-like generation (you can integrate real AI here)
      let text = '';
      
      if (fieldType === 'expectedResults') {
        text = `• Aumento de 30-50% no engajamento orgânico nas primeiras 8 semanas
• Crescimento de 20-35% na base de seguidores mensalmente
• Melhoria no posicionamento digital da marca no nicho
• Maior reconhecimento e autoridade no mercado
• Conversões aumentadas através de conteúdo estratégico`;
      } else if (fieldType === 'customNotes') {
        text = `Esta proposta foi elaborada considerando as necessidades específicas e o perfil do seu negócio. Todos os serviços são personalizáveis e adaptáveis conforme a evolução da parceria.

Nosso compromisso é com resultados reais e mensuráveis. Trabalhamos com transparência total, relatórios mensais e reuniões estratégicas para alinhamento contínuo.

Estamos prontos para iniciar e transformar sua presença digital!`;
      }
      
      return NextResponse.json({ text }, { headers: corsHeaders() });
    }

    return NextResponse.json(
      { error: 'Route not found' },
      { status: 404, headers: corsHeaders() }
    );
  } catch (error) {
    console.error('POST Error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500, headers: corsHeaders() }
    );
  }
}

export async function PUT(request) {
  try {
    const { db } = await connectToDatabase();
    const { pathname } = new URL(request.url);
    const path = pathname.replace('/api/', '');
    const body = await request.json();

    // Update proposal
    if (path.startsWith('proposals/')) {
      const id = path.split('/')[1];
      const updateData = {
        ...body,
        updatedAt: new Date().toISOString(),
      };

      delete updateData.id;
      delete updateData.createdAt;

      const result = await db
        .collection('proposals')
        .updateOne({ id }, { $set: updateData });

      if (result.matchedCount === 0) {
        return NextResponse.json(
          { error: 'Proposal not found' },
          { status: 404, headers: corsHeaders() }
        );
      }

      const proposal = await db.collection('proposals').findOne({ id });
      return NextResponse.json({ proposal }, { headers: corsHeaders() });
    }

    return NextResponse.json(
      { error: 'Route not found' },
      { status: 404, headers: corsHeaders() }
    );
  } catch (error) {
    console.error('PUT Error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500, headers: corsHeaders() }
    );
  }
}

export async function DELETE(request) {
  try {
    const { db } = await connectToDatabase();
    const { pathname } = new URL(request.url);
    const path = pathname.replace('/api/', '');

    // Delete proposal
    if (path.startsWith('proposals/')) {
      const id = path.split('/')[1];
      const result = await db.collection('proposals').deleteOne({ id });

      if (result.deletedCount === 0) {
        return NextResponse.json(
          { error: 'Proposal not found' },
          { status: 404, headers: corsHeaders() }
        );
      }

      return NextResponse.json(
        { message: 'Proposal deleted successfully' },
        { headers: corsHeaders() }
      );
    }

    return NextResponse.json(
      { error: 'Route not found' },
      { status: 404, headers: corsHeaders() }
    );
  } catch (error) {
    console.error('DELETE Error:', error);
    return NextResponse.json(
      { error: error.message },
      { status: 500, headers: corsHeaders() }
    );
  }
}
