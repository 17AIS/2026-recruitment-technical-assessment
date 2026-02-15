//
//  BuildingLoader.swift
//  FreeroomsAssessment
//
//  Created by Anh Nguyen on 31/1/2025.
//

import Foundation

public class BuildingLoader {
    private var client: HttpClient
    private var url: URL
    
    public enum Error: Swift.Error {
        case connectivity, invalidData
    }
    
    public typealias Result = Swift.Result<[Building], Swift.Error>
    
    public init(client: HttpClient, url: URL) {
        self.client = client
        self.url = url
    }
    
    public func fetchBuildings() async -> Result  {

            
        let result = await client.get(from: self.url)
        
        switch result {
        case .success(let (data, response)):
                guard response.statusCode == 200 else  {
                        return .failure(Error.invalidData)
                    }
                
                let decoder = JSONDecoder()
            return .success([])
//            let buildings: [Building] = try! decoder.decode([Building].self, from: data)
                
        case .failure(let error):
            return .failure(Error.connectivity)
        }
//            guard response?.statusCode == 200 else {
//                return .failure(Error.invalidData)
//            }
            
                
//        return .failure(Error.invalidData)
    }
}

