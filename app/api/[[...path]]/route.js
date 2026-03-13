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