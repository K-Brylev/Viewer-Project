import { gql } from '@apollo/client'

export const GET_ITEMS = gql`
  query GetItems(
    $search: String
    $categories: [ItemCategory!]
    $tradeable: Boolean
    $outdoor: Boolean
    $dyeable: Boolean
    $limit: Int
    $offset: Int
  ) {
    page(
      filter: {
        search: $search
        categories: $categories
        tradeable: $tradeable
        outdoor: $outdoor
        dyeable: $dyeable
      }
      limit: $limit
      offset: $offset
    ) {
      hasMore
      items{
        id
        name
        category
        subCategory
        description
        icon
        dyeable
        tradeable
        outdoor
        tags
        patch
      }
      
    }
  }
`
export const GET_ITEM = gql`
  query GetItem($id: Int!) {
    page(id: $id) {
      items{
        id
        name
        category
        subCategory
        description
        dyeable
        tradeable
        outdoor
        tags
        patch
        icon
      }
    }
  }
`